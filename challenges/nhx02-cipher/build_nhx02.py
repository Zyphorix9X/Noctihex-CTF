from pathlib import Path
import base64
import sys
import hashlib


if len(sys.argv) != 3:
    print("Usage: python build_nhx02.py FLAG EVIDENCE")
    raise SystemExit(1)


flag = sys.argv[1]
evidence = sys.argv[2]

BASE_DIR = Path(__file__).resolve().parent
CHALLENGE_DIR = BASE_DIR / "challenge"

CHALLENGE_DIR.mkdir(parents=True, exist_ok=True)

output_file = CHALLENGE_DIR / "dusk_message.txt"


def caesar(text, shift):
    result = []

    for ch in text:
        if "a" <= ch <= "z":
            result.append(
                chr((ord(ch) - ord("a") + shift) % 26 + ord("a"))
            )

        elif "A" <= ch <= "Z":
            result.append(
                chr((ord(ch) - ord("A") + shift) % 26 + ord("A"))
            )

        else:
            result.append(ch)

    return "".join(result)


plaintext = (
    f"Flag: {flag}\n"
    f"Evidence fragment: {evidence}\n"
    "Source: HEX-SHADOW dusk transmission\n"
)

# First layer: Caesar shift
shifted = caesar(plaintext, 5)

# Second layer: Base64 encoding
encoded = base64.b64encode(
    shifted.encode()
).decode()

output_file.write_text(
    encoded + "\n",
    encoding="utf-8"
)

sha256 = hashlib.sha256(
    output_file.read_bytes()
).hexdigest()

print(f"[+] Created: {output_file}")
print(f"[+] SHA256 : {sha256}")