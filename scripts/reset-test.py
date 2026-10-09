"""Prove that recreation removes temporary state without touching CTFd storage."""
import json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(*args):
    r=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=60)
    if r.returncode:raise RuntimeError(r.stderr.strip()[:300])
    return r.stdout.strip()
def main():
    results=[]
    for stage in ('nhx03','nhx05'):
        before=run('docker','compose','ps','-q',stage)
        key_before=run('docker','compose','exec','-T','nhx05','cat','/etc/ssh/hostkeys/ssh_host_ed25519_key.pub') if stage=='nhx05' else None
        run('docker','compose','exec','-T',stage,'sh','-c','printf reset-check > /tmp/member4-reset-check')
        run('docker','compose','exec','-T',stage,'test','-f','/tmp/member4-reset-check')
        run('docker','compose','up','-d','--no-deps','--force-recreate',stage)
        after=run('docker','compose','ps','-q',stage)
        run('docker','compose','exec','-T',stage,'test','!','-e','/tmp/member4-reset-check')
        if not before or before==after:raise RuntimeError(stage+' container was not replaced')
        if stage=='nhx05':
            for attempt in range(15):
                try:
                    key_after=run('docker','compose','exec','-T','nhx05','cat','/etc/ssh/hostkeys/ssh_host_ed25519_key.pub')
                    break
                except RuntimeError:
                    if attempt==14:raise
                    time.sleep(1)
            if key_after!=key_before:raise RuntimeError('NHX-05 SSH identity changed during normal reset')
        results.append({'stage':stage,'status':'PASS','before_container':before,'after_container':after,'actual':'Disposable marker absent after recreation'})
    run('docker','compose','restart','nginx')
    directory=ROOT/'testing/reset-tests';directory.mkdir(parents=True,exist_ok=True)
    (directory/'container-recreation.json').write_text(json.dumps(results,indent=2))
    print('Temporary-state reset checks passed. Run player-flow-test.py to verify restored challenge behavior.')
if __name__=='__main__':main()
