# Recorded testing environment

Member 4 student ID: IT24102622. Student name was not supplied.
Date: 9 October 2026 (Asia/Colombo).

Existing user-entered workstation specification (not independently verified):
Windows 26H2; AMD Ryzen 5 8645HS; 16 GB RAM; Ubuntu-24.04 WSL;
Docker Engine 29.8.0; Compose v5.5.1; global Python 3.14.7; Git 2.49.0.

Observed in this session: CTFd 3.8.8 (real export metadata), Nginx 1.31.6
(HTTP server header), Requests 2.34.2, Cryptography 50.0.2, Paramiko 5.0.0.
Validation executed with the bundled Python 3.12.14 runtime and workspace packages.
A working project .venv was subsequently created with the same runtime and pinned
dependencies. Global Python virtual-environment creation failed; Docker/WSL control
is denied.

Live endpoints: loopback HTTPS 443 and SSH 2225. Player mode: individual users.
Source revision: c658a4ca3b0e164177f8ee89e8615b5126cdbf5c plus local changes, not committed.
No Git push or commit was performed. Current certificate requires Nginx restart.
