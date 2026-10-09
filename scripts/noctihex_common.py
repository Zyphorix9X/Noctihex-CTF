"""Organizer helpers. Never upload this module or organizer solutions as player files."""
from pathlib import Path
import base64
import codecs
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = {
    'NHX-01': 'challenges/nhx01-whispers/challenge/midnight_signal.png',
    'NHX-02': 'challenges/nhx02-cipher/challenge/dusk_message.txt',
    'NHX-04': 'challenges/nhx04-packet-midnight/challenge/midnight_traffic.pcap',
    'NHX-06': 'challenges/nhx06-nocticore/challenge/nocticore',
}

def environment():
    result = {}
    for line in (ROOT / '.env').read_text().splitlines():
        if line.strip() and not line.lstrip().startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip().strip('\"\'')
    return result

def recover(text):
    flag = re.search(r'NOCTIHEX\{[^}\r\n]+\}', text)
    fragment = re.search(r'(?:Evidence fragment:\s*|fragment=)([^\s&|\r\n]+)', text)
    if not flag or not fragment:
        raise ValueError('Artifact does not contain the expected synthetic flag and fragment')
    return flag.group(), fragment.group(1)

def static_answers():
    with zipfile.ZipFile(ROOT / ARTIFACTS['NHX-01']) as archive:
        first = recover(archive.read('evidence.txt').decode())
    outer = base64.b64decode((ROOT / ARTIFACTS['NHX-02']).read_text(), validate=False).decode()
    plain = ''.join(chr((ord(c)-ord('a')-5)%26+ord('a')) if 'a'<=c<='z' else
                    chr((ord(c)-ord('A')-5)%26+ord('A')) if 'A'<=c<='Z' else c for c in outer)
    second = recover(plain)
    # Validate record boundaries before inspecting the synthetic capture payloads.
    capture = (ROOT / ARTIFACTS['NHX-04']).read_bytes()
    if capture[:4] != b'\xd4\xc3\xb2\xa1':
        raise ValueError('Expected little-endian PCAP')
    offset, records, payloads = 24, 0, []
    while offset < len(capture):
        if offset + 16 > len(capture):
            raise ValueError('Truncated PCAP record header')
        _, _, size, original = struct.unpack_from('<IIII', capture, offset)
        offset += 16
        if size > original or offset + size > len(capture):
            raise ValueError('Truncated PCAP packet')
        payloads.append(capture[offset:offset+size])
        offset += size
        records += 1
    suspicious = [p for p in payloads if b'POST /sync ' in p and b'HEX-SHADOW' in p]
    if len(suspicious) != 1 or records < 3:
        raise ValueError('Expected a unique suspicious stream and decoys')
    fourth = recover(suspicious[0].decode('latin1'))
    return {'NHX-01': first, 'NHX-02': second, 'NHX-04': fourth}

def chain_check(chain):
    value = 0x3132
    for i, byte in enumerate(chain.encode()):
        value = (((value << 5) | (value >> 27)) & 0xffffffff) ^ byte
        value = (value + i * 17) & 0xffffffff
    return value

def organizer_answers():
    answers = static_answers()
    env = environment()
    answers['NHX-03'] = env['NHX03_FLAG'], env['NHX03_EVIDENCE']
    answers['NHX-05'] = env['NHX05_FLAG'], env['NHX05_EVIDENCE']
    source = (ROOT / 'challenges/nhx06-nocticore/build/nocticore.c').read_text()
    encoded = re.search(r'encoded_flag\[\]\s*=\s*\{(.*?)\}', source, re.S).group(1)
    flag = ''.join(chr(int(n, 16) ^ 0x5a) for n in re.findall(r'0x([\da-fA-F]+)', encoded))
    if not re.fullmatch(r'NOCTIHEX\{[^}]+\}', flag):
        raise ValueError('Capstone author source flag format is invalid')
    answers['NHX-06'] = flag, ''
    return answers
