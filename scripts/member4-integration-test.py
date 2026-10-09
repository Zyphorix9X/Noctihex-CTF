"""Repeatable integration checks; blocked checks are never counted as passes.

AI-assisted implementation: Member 4 must review, understand and adapt this code.
Default mode is read-only. --offline performs artifact/source checks without Docker.
"""
import argparse
import ast
import csv
import hashlib
import json
import re
import socket
import ssl
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.request import build_opener, HTTPSHandler, ProxyHandler
from urllib.error import HTTPError
from noctihex_common import ROOT, ARTIFACTS, organizer_answers, chain_check

RESULTS = []

def record(test_id, test, status, actual):
    RESULTS.append(dict(test_id=test_id, test=test, status=status, actual=actual))
    print(f'[{status}] {test_id}: {test} — {actual}')

def check(test_id, title, function):
    try:
        actual = function()
        record(test_id, title, 'PASS', str(actual))
    except PermissionError as error:
        record(test_id, title, 'BLOCKED', str(error))
    except Exception as error:
        record(test_id, title, 'FAIL', str(error))

def command(*args):
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=45)
    if result.returncode:
        if 'permission denied' in result.stderr.lower() or 'access is denied' in result.stderr.lower():
            raise PermissionError('Session cannot access Docker/WSL control connection')
        raise RuntimeError(result.stderr.strip()[:250] or 'Command failed')
    return result.stdout

def require(condition, message):
    if not condition:
        raise AssertionError(message)

def artifacts():
    recovered = organizer_answers()
    chain = '|'.join(recovered[f'NHX-{i:02}'][1] for i in range(1, 6))
    source = (ROOT / 'challenges/nhx06-nocticore/build/nocticore.c').read_text()
    expected = int(re.search(r'expected_check\s*=\s*0x([\da-fA-F]+)', source).group(1), 16)
    require(chain_check(chain) == expected, 'Earlier evidence does not match capstone source')
    require(chain_check('WRONG|' + chain) != expected, 'Wrong chain unexpectedly accepted')
    binary = (ROOT / ARTIFACTS['NHX-06']).read_bytes()
    require(binary[:5] == b'\x7fELF\x02', 'Capstone must be ELF64')
    require(not re.search(rb'NOCTIHEX\{[^}]+\}', binary), 'Plaintext capstone flag leaked')
    return 'Three static paths recover answers; E01–E05 match author source; ELF64 has no plaintext flag. Binary execution is a separate check.'

def syntax():
    for path in ROOT.rglob('*.py'):
        if any(part in ('.venv', '__pycache__', 'private') for part in path.parts):
            continue
        require(bool(path.read_text().strip()), f'Empty Python file: {path.relative_to(ROOT)}')
        ast.parse(path.read_text(encoding='utf-8-sig'))
    return 'All project Python files contain parseable code'

def hashes(downloads):
    baseline = json.loads((ROOT / 'testing/hashes/approved-sha256.json').read_text())
    for stage, relative in ARTIFACTS.items():
        source = ROOT / relative
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        require(digest == baseline[stage]['sha256'], f'{stage}: source changed from recorded baseline')
        if downloads:
            copy = downloads / source.name
            require(copy.is_file(), f'{stage}: player download missing')
            require(hashlib.sha256(copy.read_bytes()).hexdigest() == digest, f'{stage}: download differs')
    return 'Four approved source fingerprints match' + ('; player downloads also match' if downloads else '; player delivery not checked')

def services():
    ids = command('docker', 'compose', 'ps', '-aq').split()
    require(len(ids) == 7, 'Expected seven Compose containers')
    containers = json.loads(command('docker', 'inspect', *ids))
    names = set()
    for item in containers:
        name = item['Config']['Labels']['com.docker.compose.service']
        names.add(name)
        require(item['State']['Running'], f'{name} stopped')
        config = item['HostConfig']
        require(not config['Privileged'], f'{name} privileged')
        for mount in item['Mounts']:
            require('docker.sock' not in mount['Destination'], f'{name} mounts Docker socket')
        ports = item['NetworkSettings']['Ports'] or {}
        for port, bindings in ports.items():
            if bindings:
                require(name in ('nginx', 'ssh_gateway'), f'{name} has unexpected published port')
                require(all(p['HostIp'] == '127.0.0.1' for p in bindings), f'{name} is not loopback-bound')
        if name in ('nhx03', 'nhx05'):
            require(config['Memory'] > 0 and config['PidsLimit'] > 0, f'{name} missing resource limits')
            require(all(name=='nhx05' and m['Type']=='volume' and m['Destination']=='/etc/ssh/hostkeys' for m in item['Mounts']), f'{name} has an unexpected host/data mount')
    require(names == {'mysql','redis','ctfd','nginx','nhx03','nhx05','ssh_gateway'}, 'Unexpected services')
    return 'Seven containers running; host exposure limited to loopback; challenge resource restrictions present'

def challenge_networks():
    ids = command('docker','compose','ps','-q','nhx03','nhx05').split()
    require(len(ids)==2,'Expected both live challenge containers')
    containers=json.loads(command('docker','inspect',*ids))
    network_ids={network['NetworkID'] for c in containers for network in c['NetworkSettings']['Networks'].values()}
    networks=json.loads(command('docker','network','inspect',*network_ids))
    external=[n['Name'] for n in networks if not n['Internal']]
    require(not external,'Vulnerable challenge attached to ordinary outbound network: '+', '.join(external))
    return 'Both challenge containers attach only to internal networks; separate live connection checks are still required'

def web(base, ca, path, marker):
    context = ssl.create_default_context(cafile=str(ca))
    opener = build_opener(ProxyHandler({}), HTTPSHandler(context=context))
    response = opener.open(base + path, timeout=10)
    require(response.status == 200, 'Expected HTTP 200')
    require('/setup' not in response.url, 'CTFd first-run setup is unfinished')
    require(marker.lower() in response.read().decode().lower(), 'Expected page content missing')
    return 'Expected page returned through verified HTTPS'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--base-url', default='https://noctihex.local')
    parser.add_argument('--ca', type=Path, default=ROOT/'platform/nginx/tls/noctihex.crt')
    parser.add_argument('--downloads', type=Path)
    parser.add_argument('--output', type=Path, default=ROOT/'testing/test-results')
    args = parser.parse_args()
    check('A01','Static artifacts and evidence chain',artifacts)
    check('A02','Python sources',syntax)
    check('A03','Artifact fingerprints',lambda:hashes(args.downloads))
    if not args.offline:
        check('L01','Docker service restrictions',services)
        check('L04','Challenge network configuration',challenge_networks)
        check('L02','Platform HTTPS',lambda:web(args.base_url,args.ca,'/','NoctiHex'))
        check('L03','NHX-03 HTTPS',lambda:web(args.base_url,args.ca,'/labs/nhx03/','login'))
    else:
        record('L00','Live checks','NOT RUN','Offline mode was selected')
    try:
        commit = command('git','rev-parse','HEAD').strip()
    except Exception:
        commit = 'unavailable'
    timestamp = datetime.now(timezone(timedelta(hours=5,minutes=30)))
    args.output.mkdir(parents=True, exist_ok=True)
    stem = timestamp.strftime('integration-%Y%m%d-%H%M%S')
    metadata = {'timestamp':timestamp.isoformat(),'source_commit':commit,'working_tree':'Local changes may be present','tests':RESULTS}
    (args.output/(stem+'.json')).write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    with (args.output/(stem+'.csv')).open('w',newline='',encoding='utf-8') as file:
        writer=csv.DictWriter(file,fieldnames=['test_id','test','status','actual'])
        writer.writeheader(); writer.writerows(RESULTS)
    return 1 if any(r['status'] in ('FAIL','BLOCKED') for r in RESULTS) else 0

if __name__ == '__main__':
    raise SystemExit(main())
