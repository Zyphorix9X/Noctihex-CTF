# Member 2 — Challenge Design A Evidence

**Assignment:** IE3132 Penetration Testing – Assignment 02  
**Member:** IT24103633  
**Component:** NoctiHex Challenge Design A

## Evidence Index

| ID | Evidence | Description |
|---|---|---|
| M2-01 | Git Commit History | Shows repository commits related to the implementation of NHX-01, NHX-02, and NHX-03. |
| M2-02 | NHX-01 File and Metadata Analysis | Shows analysis of `midnight_signal.png` using file inspection and metadata analysis tools. |
| M2-03 | NHX-01 Embedded Evidence Extraction | Demonstrates successful extraction of the hidden evidence artifact, stage flag, and evidence fragment from `midnight_signal.png`. |
| M2-04 | NHX-02 Base64 and Caesar Decoding | Demonstrates the intended NHX-02 solution path by decoding the Base64 layer and reversing the Caesar transformation to recover the flag and evidence fragment. |
| M2-05 | NHX-03 Login Page | Shows the running Flask web challenge and the participant login interface. |
| M2-06 | NHX-03 Container Running | Confirms that the NHX-03 Flask challenge container is successfully deployed and running. |
| M2-07 | NHX-03 IDOR Exploitation | Demonstrates the intended broken access control / IDOR vulnerability by accessing another profile through modification of the profile identifier. |
| M2-08 | NHX-03 Solver Execution | Shows successful execution of the self-developed NHX-03 solver and recovery of the challenge flag. |
| M2-09 | NHX-03 Reset and Recovery | Demonstrates successful recreation of the NHX-03 container and restoration of the challenge to its original state. |
| M2-10 | Contribution Summary | Documents the technical responsibilities and implemented work for NHX-01, NHX-02, and NHX-03. |

## Challenge Responsibilities

### NHX-01 — Whispers in the Static
- Designed and implemented the steganography and file-analysis challenge.
- Created the `midnight_signal.png` challenge artifact.
- Implemented metadata clues and embedded evidence.
- Tested the intended extraction and flag recovery path.

### NHX-02 — Cipher at Dusk
- Designed and implemented the layered cryptography challenge.
- Applied a Caesar-style transformation followed by Base64 encoding.
- Tested the reverse decoding process.
- Verified successful recovery of the flag and evidence fragment.

### NHX-03 — Mirror Account
- Developed the Flask-based web security challenge.
- Implemented the intentionally vulnerable IDOR / broken access control logic.
- Configured the Docker-based challenge environment.
- Developed and tested the solver script.
- Verified successful exploitation, flag recovery, and container reset.

## Verification

All evidence screenshots were captured from the actual NoctiHex implementation after executing the corresponding commands and challenge solution paths.

The challenge source code, Docker configuration, challenge-generation scripts, solver code, and implementation files are available in the repository under the relevant `challenges/` directories.

The submitted evidence demonstrates the implementation, testing, solution path, and individual technical contribution for NHX-01, NHX-02, and NHX-03.