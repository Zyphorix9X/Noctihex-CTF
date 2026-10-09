"""Create/update the six local NoctiHex challenges using an organizer session.

Flags are read privately from delivered artifacts and .env. Credentials are never
printed. Existing instance: set CTFD_ADMIN_NAME and CTFD_ADMIN_PASSWORD, or use
private/local-accounts.json. This script does not initialize an existing database.
"""
import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit
import requests
from noctihex_common import ROOT, ARTIFACTS, organizer_answers

class Platform:
    def __init__(self, base, ca):
        if urlsplit(base).hostname not in ('noctihex.local','127.0.0.1','localhost'):
            raise ValueError('Only the local training platform is supported')
        self.base=base.rstrip('/')
        self.session=requests.Session()
        self.session.trust_env=False
        self.session.verify=str(ca)

    def get(self,path):
        response=self.session.get(self.base+path,timeout=20)
        response.raise_for_status(); return response

    def nonce(self,path='/challenges'):
        html=self.get(path).text
        match=re.search(r'name="nonce"[^>]*value="([^"]+)"',html) or re.search(r"'csrfNonce':\s*\"([^\"]+)\"",html)
        if not match: raise RuntimeError('CSRF nonce was not found')
        return match.group(1)

    def login(self,name,password):
        nonce=self.nonce('/login')
        response=self.session.post(self.base+'/login',data={'name':name,'password':password,'nonce':nonce},timeout=20)
        response.raise_for_status()
        if urlsplit(response.url).path=='/login': raise RuntimeError('Organizer login failed')
        self.session.headers['CSRF-Token']=self.nonce('/admin/challenges')

    def api(self,method,path,**kwargs):
        response=self.session.request(method,self.base+'/api/v1'+path,timeout=30,**kwargs)
        response.raise_for_status()
        value=response.json()
        if not value.get('success'): raise RuntimeError('CTFd rejected operation: '+str(value.get('errors')))
        return value['data']

def configure(platform):
    content=json.loads((ROOT/'scripts/platform-content.json').read_text(encoding='utf-8'))
    answers=organizer_answers()
    existing={item['name']:item for item in platform.api('GET','/challenges')}
    ids={}
    for item in content:
        stage=item['stage']
        body={key:item[key] for key in ('name','category','value','description')}
        body.update(type='standard',state='visible',max_attempts=0)
        body['connection_info']=item.get('connection_info','')
        if item['name'] in existing:
            challenge_id=existing[item['name']]['id']
            platform.api('PATCH',f'/challenges/{challenge_id}',json=body)
        else:
            challenge_id=platform.api('POST','/challenges',json=body)['id']
        ids[stage]=challenge_id
        flags=platform.api('GET',f'/challenges/{challenge_id}/flags')
        desired={'challenge':challenge_id,'type':'static','content':answers[stage][0],'data':'case_sensitive'}
        if not flags: platform.api('POST','/flags',json=desired)
        elif len(flags)==1: platform.api('PATCH',f"/flags/{flags[0]['id']}",json=desired)
        else: raise RuntimeError(f'{stage} has multiple existing flags; review manually')
        hints=platform.api('GET',f'/challenges/{challenge_id}/hints')
        for cost,text in item['hints']:
            found=next((h for h in hints if h.get('content')==text),None)
            desired={'challenge_id':challenge_id,'cost':cost,'content':text}
            if found: platform.api('PATCH',f"/hints/{found['id']}",json=desired)
            else: platform.api('POST','/hints',json=desired)
        if stage in ARTIFACTS:
            files=platform.api('GET',f'/challenges/{challenge_id}/files')
            artifact=ROOT/ARTIFACTS[stage]
            if not any(f.get('location','').endswith('/'+artifact.name) for f in files):
                with artifact.open('rb') as stream:
                    platform.api('POST','/files',data={'challenge_id':challenge_id,'type':'challenge','nonce':platform.session.headers['CSRF-Token']},files={'file':(artifact.name,stream)})
        print(f'{stage}: challenge, exact flag, hints and player access configured')
    # Preserve the proposal's independently accessible story stages.
    for i,item in enumerate(content):
        platform.api('PATCH',f"/challenges/{ids[item['stage']]}",json={'next_id':ids[content[i+1]['stage']] if i+1<len(content) else None})
    return ids

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default='https://noctihex.local')
    parser.add_argument('--ca',type=Path,default=ROOT/'platform/nginx/tls/noctihex.crt')
    args=parser.parse_args()
    accounts=ROOT/'private/local-accounts.json'
    credentials=json.loads(accounts.read_text())['admin'] if accounts.exists() else {}
    name=os.getenv('CTFD_ADMIN_NAME',credentials.get('name',''))
    password=os.getenv('CTFD_ADMIN_PASSWORD',credentials.get('password',''))
    if not name or not password: parser.error('Provide organizer credentials privately')
    platform=Platform(args.base_url,args.ca)
    platform.login(name,password)
    configure(platform)

if __name__=='__main__': main()
