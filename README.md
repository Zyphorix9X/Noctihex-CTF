# NoctiHex — Echoes of the Dark Network

Six synthetic cybersecurity stages, 1,400 points before hints. This repository
contains organizer source and solutions. Players receive only the four artifacts
and the specified local web/SSH endpoints.

## Requirements

Windows 11, Docker Desktop using Linux containers, WSL2, Git, Python 3.12 or newer.
The recorded workstation has 16 GB RAM. Use an isolated local training machine.
The project publishes only `127.0.0.1:80`, `127.0.0.1:443`, and
`127.0.0.1:2225`. The approved SSH gateway confines NHX-05 to an internal network.
Apply and verify this new configuration before describing isolation as working;
see the completion script below and `docs/risk-register.csv`.

## Prepare and start

Run PowerShell from this repository. Preserve an existing `.env`:

```powershell
# Only for a new checkout:
Copy-Item .env.example .env
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r scripts/requirements.txt
.\.venv\Scripts\python.exe scripts/setup-local-cert.py
docker compose config --quiet
docker compose build
docker compose up -d
docker compose ps
```

Populate all eight `.env` values privately. Database passwords and session secrets
must be non-placeholder values. NHX-03/05 flags and evidence must match the author
artifacts and the NoctiCore verifier; do not arbitrarily change fragments.
The supplied private instructor package includes the working local `.env`.

The environment's global Python failed virtual-environment creation
(`Failed to find real location ...`). A working project `.venv` has now been created
using the bundled Python 3.12.14 runtime and the required dependencies installed.
Use `.\.venv\Scripts\python.exe` in this existing checkout. For another machine,
create the environment using a functioning Python installation. This does not prove
the reported global Python installation works.

For the hostname, add `127.0.0.1 noctihex.local` to the Windows hosts file if absent.
That system file requires administrator access. `setup-local-cert.py` generates
SANs for `noctihex.local`, `localhost` and `127.0.0.1`; it does not change Windows
trust settings. Restart Nginx after generating a certificate:

```powershell
docker compose restart nginx
```

Project Python scripts explicitly trust `platform/nginx/tls/noctihex.crt` and
verify the hostname. For normal browser access, use your approved local certificate
trust procedure. Do not permanently disable verification. TLS activation is
separately recorded in the completion status.

## Configure CTFd

Open `https://noctihex.local`. For a new deployment, complete first-time setup:
individual users, a separate organizer administrator, private challenge visibility
for unauthenticated visitors, local training registration, and no email/newsletter
integration. Keep dates unset for demonstration access.

Then configure all stages:

```powershell
.\.venv\Scripts\python.exe scripts/configure-platform.py
```

This reads the existing local organizer login from ignored
`private/local-accounts.json`. On another deployment, supply `CTFD_ADMIN_NAME` and
`CTFD_ADMIN_PASSWORD` in that shell's environment, or create a private account file
using the documented JSON structure. Do not store credentials in Git.

The script reads `scripts/platform-content.json`, author artifacts and `.env`,
creates or updates challenge metadata/flags/hints, and uploads only approved
participant artifacts. Story stages are independently visible. Next-stage
recommendations guide progression; NoctiCore needs E01–E05.
Existing conflicting flags/hints/files require organizer review. Existing files
are not overwritten by this setup helper; rerun player hash checks after changes.

| Stage | Domain | Difficulty | Points | Hints |
|---|---|---|---:|---|
| NHX-01 | Steganography | Easy | 100 | 5 / 10 |
| NHX-02 | Cryptography | Easy | 100 | 5 / 10 |
| NHX-03 | Web Security | Moderate | 200 | 10 / 20 |
| NHX-04 | Network Forensics | Moderate | 200 | 10 / 20 |
| NHX-05 | Linux/System Security | Moderate–Hard | 300 | 15 / 30 |
| NHX-06 | Reverse Engineering | Hard | 500 | 20 / 40 / 60 |

## Player access

- CTFd: `https://noctihex.local`.
- NHX-03: `https://noctihex.local/labs/nhx03/`, training login `tester / noctihex123`.
- NHX-05: `ssh analyst@127.0.0.1 -p 2225`, training password `nocti2026`.
- NHX-06: download the ELF; run it in Linux/WSL with one quoted evidence-chain
  argument. Its verifier uses stage order and `|` separators.

Organizer/test account credentials are in the ignored private account file.
The public README contains no organizer passwords or complete challenge answers.

## Integration tests

Apply the approved gateway and run primary isolation, reset, player-flow and
separate backup-recovery validation in one sequence:

```powershell
.\scripts\finish-local.ps1
```

This rebuilds/recreates NHX-05, starts the gateway, restarts Nginx, verifies the SSH
identity against the actual container, probes controlled local network destinations
before and after reset, runs player checks, exports the platform and restores it
into `noctihex-recovery` using separate database storage and ports. It stops on a
failed step. Expect several minutes plus build/download time. It preserves the
main CTFd data, does not commit or push, and saves a transcript in testing/.
This sequence has not run in the assistant sandbox because Docker control is denied.

```powershell
.\.venv\Scripts\python.exe scripts/member4-integration-test.py --offline
.\.venv\Scripts\python.exe scripts/member4-integration-test.py --downloads testing/downloads
.\.venv\Scripts\python.exe scripts/enroll-ssh-host.py
.\.venv\Scripts\python.exe scripts/player-flow-test.py
```

The first runner performs read-only checks, writes dated CSV/JSON results, and exits
nonzero for failures/blocked access. Approved artifact hashes are recorded separately
from downloads. The player-flow test creates two fresh synthetic local accounts,
validates flags and scoring, purchases first hints, checks downloads, tests NHX-03
and SSH, executes the actual ELF in the Linux lab, and exports a private backup.
It leaves test scores/accounts for evidence. It does not erase existing data.
Review its actions before running. A complete player run takes approximately two
minutes to respect submission rate limits.

## Reset

```powershell
.\scripts\reset.ps1 nhx03
.\scripts\reset.ps1 nhx05
.\scripts\reset.ps1 all
.\.venv\Scripts\python.exe scripts/reset-test.py
```

Recreation removes disposable live-container state and preserves CTFd volumes.
Nginx restarts after NHX-03 replacement to refresh upstream addresses. Check login
and intended solutions after resetting. Static stages reset by downloading the
approved originals and comparing hashes. NHX-05's new SSH identity persists across
normal resets. Applying the gateway changes that identity once; the test enrollment
script checks it against the actual local container before saving it. Your normal
SSH client's known-host file is separate and may need the same verified one-time
update. The reset test checks that the new key remains stable.

## Backup and isolated recovery

Export CTFd via Admin → Config → Backup. A real export is already saved locally in
`private/ctfd-backup.zip`; it contains accounts and answers and stays private.
Do not test import over the primary platform.

```powershell
docker compose -p noctihex-recovery -f docker-compose.yml -f testing/recovery-compose.yml config --quiet
docker compose -p noctihex-recovery -f docker-compose.yml -f testing/recovery-compose.yml up -d --build
```

The separate project has separate networks/volumes and uses HTTPS 8443 and SSH
2226. Recovery was validated by `./scripts/finish-local.ps1 -RecoveryOnly`:
the real backup restored six stages, 1400 points, 13 hints and four files into
separate database storage, followed by 59 passing recovered player checks.
The helper initializes a fresh recovery instance and imports the backup;
it refuses an unrelated existing recovery instance without its import record.
Evidence and command output are saved under testing/test-results/.
The override requires Compose 2.24.4 or newer.

Stop normally with `docker compose down`. This preserves named volumes.
`docker compose down -v` deletes platform storage; it is not an ordinary reset.

## Evidence, changes and submission

See `testing/test-cases.csv`, `testing/test-results/`, `testing/hashes/`,
`testing/defects/`, `docs/evidence-index.csv`, `docs/risk-register.csv`,
`docs/design-changes.md`, `docs/contributions.md`, and `docs/completion-status.md`.
Logs are actual test evidence, not screenshot substitutes claimed as live recording.
Screenshots and the maximum-20-minute group video are still required where your
demonstration needs them. Members must record and explain their own live segments.

Submission group name: `IT24102720_IT24103633_IT24103547_IT24102622`.
No written report is required by Assignment 02. Provide source, working box,
setup/reset README, genuine contribution evidence, and the group's live video.
Keep private setup material in the instructor package rather than a public Git push.

## Tools and attribution

Existing challenges use Flask/Werkzeug, GCC, Ubuntu, Scapy and synthetic authored
artifacts. Platform: CTFd, Nginx, MySQL, Redis, Docker Desktop/Compose and WSL.
Integration tools: Python, Requests, Cryptography and Paramiko. Analysis tools in
the intended paths include ExifTool, unzip, Wireshark, GDB/Ghidra and Git.
All challenge traffic and records are fictional. Integration work in this session
is AI-assisted and identified in the contribution record.

Official references: [CTFd challenge configuration](https://docs.ctfd.io/tutorials/challenges/creating-challenges/),
[CTFd API](https://docs.ctfd.io/docs/api/redoc/),
[CTFd backup/import](https://docs.ctfd.io/tutorials/getting-started/),
[Docker port publishing](https://docs.docker.com/engine/network/port-publishing/),
[Flask proxy handling](https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/).
