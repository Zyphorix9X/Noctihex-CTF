# NHX-05 – Misplaced Trust

## Challenge Information

- **Category:** Linux / System Security
- **Difficulty:** Moderate–Hard
- **Points:** 300
- **Environment:** Isolated Ubuntu Docker container

## Description

The participant connects to a fictional Linux backup server as a low-privilege analyst. A custom backup utility has been configured with restricted sudo permissions.

The objective is to analyze the utility's trust and path-validation behavior within the authorized CTF environment.

## Requirements

- Docker Desktop
- Docker Compose
- SSH client
- Windows PowerShell or Linux terminal

## Starting the Challenge

From the Noctihex-CTF project root:

```powershell
docker compose up -d --build nhx05
```

Check the container:

```powershell
docker compose ps nhx05
```

## Connecting

```powershell
ssh analyst@127.0.0.1 -p 2225
```

Use the analyst password configured for the local training environment.

## Intended Investigation

1. Connect to the challenge container.
2. Identify the current user.
3. Inspect the restricted sudo permissions.
4. Identify the custom backup utility.
5. Examine the utility's path-validation behavior.
6. Complete the intended local challenge and recover the flag and evidence fragment.

## Hints

**Hint 1:** Check the commands the analyst user is permitted to execute.

**Hint 2:** Investigate how the backup utility decides whether a file path is allowed.

## Reset

Exit the SSH session, then run from the project root:

```powershell
docker compose stop nhx05
docker compose rm -f nhx05
docker compose up -d --build nhx05
```

## Security

This challenge is designed for an isolated Docker training environment. SSH is bound to localhost on port 2225. Do not deploy this intentionally vulnerable service on a public network.

## Validation

- Container starts successfully.
- SSH authentication works.
- Analyst is a non-root user.
- Restricted sudo permission works.
- Normal backup operation succeeds.
- Direct access to the protected flag is denied.

The intended challenge solution and flag retrieval must also be validated before final submission.
