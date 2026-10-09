"""Verify the gateway's SSH public key against its actual local Compose container."""
import argparse,subprocess,socket
from pathlib import Path
import paramiko
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--project',default='noctihex-ctf')
parser.add_argument('--port',type=int,default=2225)
args=parser.parse_args()
expected=subprocess.run(['docker','compose','-p',args.project,'exec','-T','nhx05','cat','/etc/ssh/hostkeys/ssh_host_ed25519_key.pub'],cwd=ROOT,capture_output=True,text=True,check=True,timeout=15).stdout.split()
if len(expected)<2:raise RuntimeError('Container public key is missing')
with socket.create_connection(('127.0.0.1',args.port),timeout=5) as connection:
    transport=paramiko.Transport(connection)
    try:
        transport.start_client(timeout=10)
        key=transport.get_remote_server_key()
        if (key.get_name(),key.get_base64()) != (expected[0],expected[1]):
            raise RuntimeError('Gateway SSH identity differs from the actual container')
        destination=ROOT/'private'/('ssh-known-hosts' if args.port==2225 else f'ssh-known-hosts-{args.port}')
        destination.parent.mkdir(exist_ok=True)
        keys=paramiko.HostKeys()
        if destination.exists():keys.load(str(destination))
        # Only replace this verified local endpoint; preserve other host entries.
        host=f'[127.0.0.1]:{args.port}'
        if host in keys:del keys[host]
        keys.add(host,key.get_name(),key)
        keys.save(str(destination))
        print('SSH host identity verified against local container and saved')
    finally:transport.close()
