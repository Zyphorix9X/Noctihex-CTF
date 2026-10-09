"""Create a self-signed local TLS certificate with correct SANs.

No Windows trust settings are modified. Use the certificate explicitly as a CA
for the project scripts. Existing keys are preserved; old certificates are backed
up under the ignored private directory. Restart Nginx after running this command.
"""
from datetime import datetime,timezone,timedelta
import ipaddress
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import rsa
ROOT=Path(__file__).resolve().parents[1]

def main():
    tls=ROOT/'platform/nginx/tls';tls.mkdir(parents=True,exist_ok=True)
    private=ROOT/'private';private.mkdir(exist_ok=True)
    keypath=tls/'noctihex.key';certpath=tls/'noctihex.crt'
    if keypath.exists():
        key=serialization.load_pem_private_key(keypath.read_bytes(),password=None)
    else:
        key=rsa.generate_private_key(public_exponent=65537,key_size=3072)
        keypath.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    if certpath.exists():
        backup=private/('certificate-before-'+datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')+'.crt')
        backup.write_bytes(certpath.read_bytes())
    subject=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'noctihex.local')])
    now=datetime.now(timezone.utc)
    cert=(x509.CertificateBuilder().subject_name(subject).issuer_name(subject)
          .public_key(key.public_key()).serial_number(x509.random_serial_number())
          .not_valid_before(now-timedelta(minutes=5)).not_valid_after(now+timedelta(days=365))
          .add_extension(x509.SubjectAlternativeName([x509.DNSName('noctihex.local'),x509.DNSName('localhost'),x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]),critical=False)
          .add_extension(x509.BasicConstraints(ca=True,path_length=0),critical=True)
          .sign(key,hashes.SHA256()))
    certpath.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    print('Certificate written with noctihex.local, localhost and loopback SANs. Restart Nginx to activate it.')

if __name__=='__main__':main()
