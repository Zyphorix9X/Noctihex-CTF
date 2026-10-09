"""Probe only controlled local Docker endpoints, with reachable positive controls.

Creates one temporary HTTP canary with no published host ports and removes it in
finally. Main CTFd/challenge data and volumes are untouched.
"""
import json,subprocess,time,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args,check=True):
    r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,timeout=45)
    if check and r.returncode:raise RuntimeError(r.stderr.strip()[:300] or 'Local probe failed')
    return r
def inspect(id):return json.loads(run('docker','inspect',id).stdout)[0]
def tcp(ip,port):
    return f"import socket; s=socket.create_connection(('{ip}',{port}),3); s.close()"
def main():
    results=[]
    canary='noctihex-test-canary-'+uuid.uuid4().hex[:10]
    gateway=inspect(run('docker','compose','ps','-q','ssh_gateway').stdout.strip())
    networks=gateway['NetworkSettings']['Networks']
    access=next(n for n in networks if n.endswith('_ssh_access'))
    mysql=inspect(run('docker','compose','ps','-q','mysql').stdout.strip())
    redis=inspect(run('docker','compose','ps','-q','redis').stdout.strip())
    def record(title,success):
        results.append({'test':title,'status':'PASS' if success else 'FAIL'})
        print(results[-1]['status'],title)
        if not success:raise RuntimeError('Isolation expectation failed: '+title)
    try:
        record('NHX-03 TCP probe works on its own local listener',run('docker','compose','exec','-T','nhx03','python','-c',tcp('127.0.0.1',5000),check=False).returncode==0)
        record('NHX-05 TCP probe works on its own local SSH listener',run('docker','compose','exec','-T','nhx05','timeout','4','bash','-c','exec 3<>/dev/tcp/127.0.0.1/22',check=False).returncode==0)
        run('docker','run','-d','--name',canary,'--network',access,'--label','noctihex.temporary-test=true','python:3.13-slim','python','-m','http.server','8089')
        canary_ip=inspect(canary)['NetworkSettings']['Networks'][access]['IPAddress']
        for attempt in range(10):
            control=run('docker','run','--rm','--network',access,'python:3.13-slim','python','-c',tcp(canary_ip,8089),check=False)
            if control.returncode==0:break
            time.sleep(1)
        record('Canary reachable from ordinary access network',control.returncode==0)
        targets=[('ordinary-access canary',canary_ip,8089)]
        for title,container,port in [('MySQL',mysql,3306),('Redis',redis,6379)]:
            ip=next(iter(container['NetworkSettings']['Networks'].values()))['IPAddress']
            control=run('docker','compose','exec','-T','ctfd','python','-c',tcp(ip,port),check=False)
            record(title+' reachable from authorized backend control',control.returncode==0)
            targets.append((title,ip,port))
        for title,ip,port in targets:
            web=run('docker','compose','exec','-T','nhx03','python','-c',tcp(ip,port),check=False)
            record('NHX-03 cannot reach '+title,web.returncode!=0)
            linux=run('docker','compose','exec','-T','nhx05','timeout','4','bash','-c',f'exec 3<>/dev/tcp/{ip}/{port}',check=False)
            # 124 is timeout, 1 is bash's connection failure. Other errors are not passes.
            record('NHX-05 cannot reach '+title,linux.returncode in (1,124))
        directory=ROOT/'testing/test-results';directory.mkdir(parents=True,exist_ok=True)
        (directory/'controlled-isolation.json').write_text(json.dumps({'scope':'Controlled local endpoints only; available positive controls verified','tests':results},indent=2))
    finally:
        # Only this invocation's uniquely named, labelled canary is removed.
        found=run('docker','inspect',canary,check=False)
        if found.returncode==0:
            item=json.loads(found.stdout)[0]
            if item['Config']['Labels'].get('noctihex.temporary-test')=='true':
                run('docker','rm','-f',canary)
if __name__=='__main__':main()
