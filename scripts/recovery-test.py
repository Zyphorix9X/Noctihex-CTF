import json,subprocess,time,importlib.util,secrets
from pathlib import Path
from zipfile import ZipFile
import requests
from noctihex_common import ROOT
spec=importlib.util.spec_from_file_location('platform_setup',ROOT/'scripts/configure-platform.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def volume(project):
    id=subprocess.run(['docker','compose','-p',project,'ps','-q','mysql'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
    if not id:raise RuntimeError('MySQL container missing in '+project)
    value=json.loads(subprocess.run(['docker','inspect',id],cwd=ROOT,text=True,capture_output=True,check=True).stdout)[0]
    return next(m['Name'] for m in value['Mounts'] if m['Destination']=='/var/lib/mysql')

def main():
    if volume('noctihex-recovery')==volume('noctihex-ctf'):
        raise RuntimeError('Recovery must not share primary database storage')
    platform=module.Platform('https://127.0.0.1:8443',ROOT/'platform/nginx/tls/noctihex.crt')
    accounts=json.loads((ROOT/'private/local-accounts.json').read_text())
    for attempt in range(60):
        try:
            page=platform.get('/setup');break
        except requests.RequestException:
            if attempt==59:raise
            time.sleep(2)
    initialized='/setup' not in page.url
    marker=ROOT/'private/recovery-import-record.json'
    if initialized and not marker.exists():
        raise RuntimeError('Recovery contains existing data without this script\'s import record; inspect it before replacing anything')
    if not initialized:
        form={'ctf_name':'NoctiHex Recovery','user_mode':'users','challenge_visibility':'private','account_visibility':'public','score_visibility':'public','registration_visibility':'public','verify_emails':'false','social_shares':'false','ctf_theme':'core','start':'','end':'','nonce':platform.nonce('/setup'),**accounts['admin']}
        response=platform.session.post(platform.base+'/setup',data=form,timeout=30)
        response.raise_for_status()
        if '/setup' in response.url:raise RuntimeError('Recovery initialization failed')
    platform.login(accounts['admin']['name'],accounts['admin']['password'])
    backup=ROOT/'private/ctfd-backup.zip'
    if not initialized:
        with backup.open('rb') as file:
            response=platform.session.post(platform.base+'/admin/import',data={'nonce':platform.nonce('/admin/import')},files={'backup':(backup.name,file)},timeout=30)
            response.raise_for_status()
        marker.write_text(json.dumps({'project':'noctihex-recovery','endpoint':'https://127.0.0.1:8443','backup':'private/ctfd-backup.zip','state':'import requested'},indent=2))
    for attempt in range(60):
        try:
            platform.login(accounts['admin']['name'],accounts['admin']['password'])
            challenges=platform.api('GET','/challenges')
            if len(challenges)==6:break
        except (requests.RequestException,RuntimeError):pass
        if attempt==59:raise RuntimeError('Recovery did not restore six challenges within the timeout')
        time.sleep(2)
    hints=0;files=0
    for challenge in challenges:
        hints+=len(platform.api('GET',f"/challenges/{challenge['id']}/hints"))
        files+=len(platform.api('GET',f"/challenges/{challenge['id']}/files"))
    if sum(c['value'] for c in challenges)!=1400 or hints!=13 or files!=4:
        raise RuntimeError('Restored points, hints or player files differ')
    directory=ROOT/'testing/test-results';directory.mkdir(exist_ok=True)
    report={'status':'PASS','project':'noctihex-recovery','separate_database_volume':True,'challenge_count':6,'points':1400,'hints':13,'files':4,'actual':'Real CTFd export restored in separate Docker storage; player flow is tested next'}
    (directory/'recovery-import.json').write_text(json.dumps(report,indent=2))
    marker.write_text(json.dumps(report,indent=2))
    print('Recovery import verified: separate database, six stages, 1400 points, thirteen hints, four files')
if __name__=='__main__':main()
