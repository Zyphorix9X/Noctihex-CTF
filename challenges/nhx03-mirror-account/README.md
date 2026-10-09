# NHX-03 – Mirror Account

## Domain

Web Security / Broken Access Control

## Difficulty

Moderate

## Points

200

## Scenario

A fictional NoctiHex employee portal contains a broken object-level authorization flaw.

The participant is provided with a valid test account and must inspect how profile records are accessed.

## Participant Credentials

Username:

```text
tester
```

Password: `noctihex123` (synthetic training credentials).

## Access

Open `https://noctihex.local/labs/nhx03/`. Log in, inspect your profile URL,
and investigate object-level access control within this fictional portal.
Recover the stage flag and E03. The next story stage is NHX-04.

## Hints

### Hint 1 — 10 points
Observe the profile identifier in your browser address.

### Hint 2 — 20 points
Authentication and object-level authorization are separate checks.

## Build and reset

From the repository root, run `docker compose up -d --build nhx03`.
Reset with `./scripts/reset.ps1 nhx03`. This recreates in-memory records and
temporary container files; it does not erase CTFd scores. Existing browser cookies
remain signed by the configured secret, so logout/login is part of the reset check.

## Organizer validation

Run `python challenges/nhx03-mirror-account/solution/solver.py` with the local
certificate. Verify wrong login, unauthenticated profile requests, profile 1,
the intended profile change, logout, and CTFd flag validation.
Do not upload the author source or solution directory to players.
