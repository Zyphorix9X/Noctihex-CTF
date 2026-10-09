"""AI-assisted organizer validation; creates two fresh local test users per run.
Tests real player flag validation, hints, downloads, web and SSH intended paths.
Does not reset scores or delete accounts. Review before running.
"""
import sys,json,re,ssl,hashlib,csv,importlib.util,time,argparse
from pathlib import Path
from datetime import datetime,timezone,timedelta
from requests.adapters import HTTPAdapter
import paramiko
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url',default='https://noctihex.local')
parser.add_argument('--ssh-port',type=int,default=2225)
parser.add_argument('--report-name',default='live-player-flow')
args=parser.parse_args()
sys.path.insert(0,str(root/'scripts'))
from noctihex_common import organizer_answers,ARTIFACTS,chain_check
spec=importlib.util.spec_from_file_location('platform_setup',root/'scripts/configure-platform.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def client():
    return module.Platform(args.base_url,root/'platform/nginx/tls/noctihex.crt')
results=[]
def result(name,success,detail):
    results.append({'test':name,'status':'PASS' if success else 'FAIL','actual':detail})
    print(results[-1]['status'],name,detail)
    directory=root/'testing/test-results';directory.mkdir(parents=True,exist_ok=True)
    (directory/(args.report_name+'.json')).write_text(json.dumps({'timestamp':datetime.now(timezone(timedelta(hours=5,minutes=30))).isoformat(),'transport':'Verified local HTTPS using the project certificate','tests':results},indent=2))
accounts=json.loads((root/'private/local-accounts.json').read_text())
ids=json.loads((root/'private/challenge-ids.json').read_text())
answers=organizer_answers()
admin=client();admin.login(accounts['admin']['name'],accounts['admin']['password'])
import secrets
suffix=str(int(time.time()))
for key in ('player','hint-tester'):
    accounts[key]={'name':'noctihex-'+key+'-'+suffix,'email':'noctihex-'+key+'-'+suffix+'@example.com','password':secrets.token_urlsafe(24)}
    admin.api('POST','/users',json={**accounts[key],'type':'user','verified':True,'hidden':False,'banned':False})
(root/'private/local-accounts.json').write_text(json.dumps(accounts,indent=2))
player=client()
nonce=player.nonce('/login')
bad=player.session.post(player.base+'/login',data={'name':accounts['player']['name'],'password':'wrong-test-password','nonce':nonce},timeout=15)
result('Invalid player login', '/login' in bad.url and 'incorrect' in bad.text.lower(),'Wrong credentials rejected with login page')
def player_login(p,key):
    n=p.nonce('/login');r=p.session.post(p.base+'/login',data={**accounts[key],'nonce':n},timeout=15)
    if '/login' in r.url:raise RuntimeError('Player login failed')
    p.session.headers['CSRF-Token']=p.nonce('/challenges')
player_login(player,'player')
result('Player authentication',True,'Separate ordinary player logged in')
listing=player.api('GET','/challenges')
result('Six visible stages',len(listing)==6 and sum(x['value'] for x in listing)==1400,'Six stages totaling 1400 points')
downloads=root/'testing/downloads';downloads.mkdir(parents=True,exist_ok=True)
hashrows=[]
for stage,id in ids.items():
    challenge=player.api('GET',f'/challenges/{id}')
    if stage in ARTIFACTS:
        source=root/ARTIFACTS[stage]
        matched=False
        for url in challenge['files']:
            r=player.get(url)
            if source.name in url:
                (downloads/source.name).write_bytes(r.content)
                expected=hashlib.sha256(source.read_bytes()).hexdigest()
                actual=hashlib.sha256(r.content).hexdigest()
                matched=expected==actual
                hashrows.append(dict(stage=stage,filename=source.name,source_sha256=expected,downloaded_sha256=actual,result='PASS' if matched else 'FAIL'))
        result(stage+' player download',matched,'Player download SHA256 matches approved source' if matched else 'Download missing or changed')
    for label,submission,expected_status in [('wrong','NOCTIHEX{incorrect_test}', 'incorrect'),('cross-stage',answers['NHX-02' if stage=='NHX-01' else 'NHX-01'][0],'incorrect'),('correct',answers[stage][0],'correct'),('duplicate',answers[stage][0],'already_solved')]:
        time.sleep(5.2)
        response=player.api('POST','/challenges/attempt',json={'challenge_id':id,'submission':submission})
        result(stage+' '+label+' flag',response['status']==expected_status,'Platform response: '+response['status'])
result('No-hint total score',player.api('GET','/users/me').get('score')==1400,'Player score: '+str(player.api('GET','/users/me').get('score')))
hintplayer=client();player_login(hintplayer,'hint-tester')
content=json.loads((root/'scripts/platform-content.json').read_text())
costsum=0
for item in content:
    id=ids[item['stage']]
    detail=hintplayer.api('GET',f'/challenges/{id}')
    hints=detail['hints']
    expected=[cost for cost,_ in item['hints']]
    result(item['stage']+' hint prices',[h['cost'] for h in hints]==expected,'Player-visible hint costs match proposal')
    hintplayer.api('POST','/challenges/attempt',json={'challenge_id':id,'submission':answers[item['stage']][0]})
    for hint in hints:
        if hint['cost']!=expected[0]:continue
        try:
            hintplayer.api('POST','/unlocks',json={'target':hint['id'],'type':'hints'})
            costsum+=hint['cost']
            result(item['stage']+' hint purchase',True,'First progressive hint unlocked')
        except Exception as error:
            result(item['stage']+' hint purchase',False,str(error))
score=hintplayer.api('GET','/users/me').get('score')
result('Hint deductions',score==1400-costsum,f'Score {score}; expected {1400-costsum}')
# Intended web challenge route, negative authentication, cookies and logout.
web=client();base='/labs/nhx03'
unauth=web.get(base+'/profile/2')
result('NHX-03 unauthenticated profile', '/login' in unauth.url and 'NOCTIHEX{' not in unauth.text,'Unauthenticated request redirects without flag')
bad=web.session.post(web.base+base+'/login',data={'username':'tester','password':'wrong'},timeout=15)
result('NHX-03 wrong login','Invalid username or password' in bad.text,'Generic error displayed')
own=web.session.post(web.base+base+'/login',data={'username':'tester','password':'noctihex123'},timeout=15)
result('NHX-03 login and routing',own.url.endswith('/labs/nhx03/profile/1') and 'NOCTIHEX{' not in own.text,'Expected profile under challenge prefix; own record contains no flag')
target=web.get(base+'/profile/2')
result('NHX-03 intended solve',answers['NHX-03'][0] in target.text and answers['NHX-03'][1] in target.text,'Intended profile request recovers configured flag and E03')
cookie=next((c for c in web.session.cookies if c.name=='nhx03_session'),None)
result('NHX-03 cookie boundary',bool(cookie and cookie.secure and cookie.path=='/labs/nhx03/'),'Dedicated Secure cookie is restricted to challenge path')
web.get(base+'/logout')
result('NHX-03 logout','/login' in web.get(base+'/profile/2').url,'Logout removes authenticated access')
# SSH host key is enrolled once for this explicit local lab, then persisted and checked.
ssh=paramiko.SSHClient();known=root/'private'/('ssh-known-hosts' if args.ssh_port==2225 else f'ssh-known-hosts-{args.ssh_port}')
if not known.exists():raise RuntimeError('Run enroll-ssh-host.py to verify the server key against the local container first')
ssh.load_host_keys(str(known))
ssh.connect('127.0.0.1',port=args.ssh_port,username='analyst',password='nocti2026',look_for_keys=False,allow_agent=False,timeout=10)
ssh.save_host_keys(str(known))
def remote(command):
    _,out,err=ssh.exec_command(command,timeout=10);text=out.read().decode();error=err.read().decode();return out.channel.recv_exit_status(),text,error
code,text,_=remote('whoami');result('NHX-05 SSH player',code==0 and text.strip()=='analyst','SSH authenticates a non-root analyst')
code,text,_=remote('sudo -n -l');result('NHX-05 restricted sudo',code==0 and '/usr/local/bin/nocti-backup' in text,'Only author-configured backup sudo permission inspected')
code,text,_=remote('cat /root/flag.txt');result('NHX-05 protected file',code!=0 and not text,'Direct protected-file access denied')
code,text,_=remote('sudo -n /usr/local/bin/nocti-backup /opt/noctihex/backups/readme.txt');result('NHX-05 normal backup',code==0 and 'Nightly backup archive.' in text,'Allowed backup succeeds')
code,text,_=remote('sudo -n /usr/local/bin/nocti-backup /root/flag.txt');result('NHX-05 outside-prefix path',code!=0 and not text,'Outside-prefix path rejected')
code,text,_=remote('sudo -n /usr/local/bin/nocti-backup /opt/noctihex/backups/../../../root/flag.txt');result('NHX-05 intended solve',code==0 and answers['NHX-05'][0] in text and answers['NHX-05'][1] in text,'Intended training traversal recovers protected flag and E05')
fragment_chain='|'.join(answers[f'NHX-{i:02}'][1] for i in range(1,6))
sftp=ssh.open_sftp();binary_path='/home/analyst/member4-nocticore-verification';sftp.put(str(root/ARTIFACTS['NHX-06']),binary_path);sftp.chmod(binary_path,0o700)
import shlex
code,text,_=remote(binary_path+' '+shlex.quote(fragment_chain));result('NHX-06 Linux binary correct chain',code==0 and answers['NHX-06'][0] in text,'Delivered ELF executed in Linux and accepted E01â€“E05')
code,text,_=remote(binary_path+' '+shlex.quote('WRONG|'+fragment_chain));result('NHX-06 Linux binary wrong chain',code!=0 and 'SUCCESS' not in text and 'NOCTIHEX{' not in text,'Wrong chain exits nonzero without a flag')
sftp.remove(binary_path);sftp.close();ssh.close()
hashdir=root/'testing/hashes';hashdir.mkdir(parents=True,exist_ok=True)
with (hashdir/'player-downloads.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(hashrows[0]));w.writeheader();w.writerows(hashrows)
report={'timestamp':datetime.now(timezone(timedelta(hours=5,minutes=30))).isoformat(),'transport':'Verified local HTTPS using the project certificate','tests':results}
resultdir=root/'testing/test-results';resultdir.mkdir(parents=True,exist_ok=True)
(resultdir/(args.report_name+'.json')).write_text(json.dumps(report,indent=2))
backup=admin.get('/admin/export')
if backup.content.startswith(b'PK'):
    (root/'private'/('ctfd-backup.zip' if args.ssh_port==2225 else 'ctfd-backup-recovery.zip')).write_bytes(backup.content);print('CTFd backup saved privately')
else:raise RuntimeError('Backup endpoint did not return an export ZIP')
raise SystemExit(1 if any(t['status']!='PASS' for t in results) else 0)
