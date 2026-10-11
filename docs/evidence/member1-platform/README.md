# Member 1 — Platform and Architecture Evidence

**Assignment:** IE3132 Penetration Testing — Assignment 02  
**Member:** IT24102720  
**Component:** NoctiHex CTF Platform and Architecture

## Evidence Index

| ID | Evidence | Description |
|---|---|---|
| M1-01 | Docker Deployment | Shows the successful deployment of the CTF platform using Docker Compose. |
| M1-02 | Running Containers | Shows the running CTFd, Nginx, MySQL, Redis and challenge containers. |
| M1-03 | Platform Homepage | Confirms that the NoctiHex web platform is accessible. |
| M1-04 | Challenge List | Shows all six configured CTF challenges. |
| M1-05 | Flag Validation | Demonstrates correct and incorrect flag submission results. |
| M1-06 | Architecture | Shows the implemented platform architecture and network design. |
| M1-07 | Backend Isolation | Shows that MySQL and Redis ports are not published to the host. |
| M1-08 | Container Security | Shows that challenge containers are not running in privileged Docker mode. |
| M1-09 | Resource Monitoring | Shows CPU and memory usage of the running containers. |
| M1-10 | Logging | Shows platform log monitoring using Docker Compose. |
| M1-11 | Automation | Demonstrates the self-developed platform validation script. |
| M1-12 | Reset and Recovery | Demonstrates successful recreation and verification of a challenge container. |

## Verification

All evidence screenshots are captured from the actual implementation. Results are recorded after executing the corresponding commands.

The source code, Docker configuration, scripts and deployment instructions are available in the repository.