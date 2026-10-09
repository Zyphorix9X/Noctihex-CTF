# Design changes from the approved proposal

| Proposed | Implemented | Technical reason and validation |
|---|---|---|
| Ubuntu Server host and Kali participant VM | Windows workstation with Docker Desktop/WSL Linux containers | Existing group environment. Real web and SSH player flow is tested; it does not establish a separate participant-machine boundary. |
| PCAPNG forensic artifact | Classic PCAP | Delivered generator produces PCAP. Wireshark can inspect the synthetic traffic; player download is checked against the original SHA256. |
| SQLite web records | Flask in-memory fictional profiles | Small deterministic dataset; container recreation restores records. Session cookies must be checked separately. |
| Story progression | Independently visible stages with next-stage recommendations | Preserves the proposal's distinction between story order and hard technical dependencies. NoctiCore requires E01–E05. No prerequisite locks were added. |
| Consistent capstone hint policy | 20 / 40 / 60 in README, content configuration and CTFd | Corrected stale 10 / 20 / 30 documentation to match proposal and manifest. |
| Internal-only networks | Fixed SSH gateway preserves host access while NHX-05 uses its own internal network | User approved the change. Deployed; controlled runtime isolation checks passed after resets. The gateway forwards only to NHX-05 port 22, while web access uses the existing Nginx bridge. |
| Member scripts under scripts/ | Entry points wrap the existing author solvers | Removes empty placeholders without falsely describing the wrappers as new Member 2/3 algorithms. |

The current NoctiCore uses a 32-bit mixing check and lightweight XOR obfuscation.
This is an educational reverse-engineering mechanism; it is not cryptographic
authentication. A participant can reconstruct the algorithm and flag decoder.
The approved intended path uses earlier evidence; collision resistance is limited.

AI-assisted integration changes are listed in `docs/contributions.md`. The actual
video and each member's explanation must be produced by the members themselves.
