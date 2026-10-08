from PIL import Image, ImageDraw, PngImagePlugin
from pathlib import Path
import random
import zipfile
import hashlib
import sys


if len(sys.argv) != 3:
    print("Usage: python build_nhx01.py FLAG EVIDENCE")
    raise SystemExit(1)


flag = sys.argv[1]
evidence = sys.argv[2]

BASE_DIR = Path(__file__).resolve().parent
CHALLENGE_DIR = BASE_DIR / "challenge"

CHALLENGE_DIR.mkdir(parents=True, exist_ok=True)

output_png = CHALLENGE_DIR / "midnight_signal.png"
payload_zip = BASE_DIR / "nhx01_payload.zip"


W, H = 1280, 720

random.seed(3132)

img = Image.new(
    "RGB",
    (W, H),
    (6, 10, 20)
)

draw = ImageDraw.Draw(img)


# Create synthetic night-static background
for _ in range(4200):
    x = random.randrange(W)
    y = random.randrange(H)
    v = random.randrange(18, 75)

    draw.point(
        (x, y),
        fill=(
            v,
            min(255, v + 6),
            min(255, v + 14)
        )
    )


# Add horizontal scan lines
for y in range(0, H, 8):
    draw.line(
        (0, y, W, y),
        fill=(10, 16, 28)
    )


# Add challenge metadata
metadata = PngImagePlugin.PngInfo()

metadata.add_text(
    "Title",
    "NoctiHex Midnight Signal"
)

metadata.add_text(
    "Author",
    "NoctiHex Incident Response"
)

metadata.add_text(
    "Comment",
    "NoctiHex evidence: inspect metadata and embedded file structures"
)


img.save(
    output_png,
    pnginfo=metadata
)


# Create the hidden payload
payload_text = (
    "NOCTIHEX INCIDENT ARTIFACT\n"
    "==========================\n"
    f"Flag: {flag}\n"
    f"Evidence fragment: {evidence}\n"
    "Source: HEX-SHADOW midnight signal\n"
)


with zipfile.ZipFile(
    payload_zip,
    "w",
    zipfile.ZIP_DEFLATED
) as archive:

    archive.writestr(
        "evidence.txt",
        payload_text
    )


# Append ZIP bytes to the valid PNG
with open(output_png, "ab") as png_file:
    with open(payload_zip, "rb") as zip_file:
        png_file.write(zip_file.read())


# Delete temporary ZIP
payload_zip.unlink()


# Calculate SHA-256 hash
sha256 = hashlib.sha256(
    output_png.read_bytes()
).hexdigest()


print(f"[+] Created: {output_png}")
print(f"[+] SHA256 : {sha256}")