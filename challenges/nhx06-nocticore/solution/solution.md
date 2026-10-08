# NHX-06 — NoctiCore Author Solution

## Challenge Information

- Domain: Reverse Engineering / Linux ELF
- Difficulty: Hard
- Points: 500
- Challenge: NHX-06 — NoctiCore

## Objective

Analyze the NoctiCore Linux ELF executable, reconstruct the evidence chain from NHX-01 to NHX-05, and obtain the final flag.

## Required Tools

- Ubuntu Linux / WSL
- GCC
- `file`
- `strings`
- Python 3
- Ghidra or GDB (optional)

## Step 1 — Identify the Binary

Run:

```bash
file challenge/nocticore
```

The executable is a 64-bit Linux ELF.

## Step 2 — Inspect the Executable

Run:

```bash
strings challenge/nocticore
```

Observe the verification messages. The full flag is not stored as a plaintext string.

## Step 3 — Recover the Evidence Fragments

The development evidence values are:

| Challenge | Fragment |
|---|---|
| NHX-01 | ECHO17 |
| NHX-02 | NIGHT42 |
| NHX-03 | ARCHIVE7 |
| NHX-04 | DEV_E4 |
| NHX-05 | DEV_E5 |

The NHX-04 and NHX-05 fragments are temporary development values.

## Step 4 — Construct the Evidence Chain

Combine the fragments in stage order, separated by `|`.

```text
ECHO17|NIGHT42|ARCHIVE7|DEV_E4|DEV_E5
```

## Step 5 — Calculate the Verification Value

Run:

```bash
python3 solution/solve.py "ECHO17|NIGHT42|ARCHIVE7|DEV_E4|DEV_E5"
```

Expected output:

```text
Derived check: 0xdc071061
Evidence chain matches the development verifier.
```

The C program uses a 32-bit rotating and mixing algorithm to calculate the verification value.

## Step 6 — Execute NoctiCore

Run:

```bash
./challenge/nocticore "ECHO17|NIGHT42|ARCHIVE7|DEV_E4|DEV_E5"
```

Expected output:

```text
NoctiCore verification
Evidence verification: SUCCESS
NoctiCore unlocked.
Flag: NOCTIHEX{DEV_NHX06}
```

## Step 7 — Verify Incorrect Input

Run:

```bash
./challenge/nocticore "WRONG|NIGHT42|ARCHIVE7|DEV_E4|DEV_E5"
```

Expected output:

```text
NoctiCore verification
Evidence verification: FAILED
Incorrect evidence chain.
```

## Step 8 — Verify Flag Obfuscation

Run:

```bash
strings challenge/nocticore | grep 'NOCTIHEX'
```

Expected: No matching plaintext flag.

The development flag is XOR-obfuscated with key `0x5A`. This is lightweight obfuscation, not strong encryption.

## Reset / Recovery

NHX-06 is a static executable challenge. To reset it, rebuild from source:

```bash
gcc -O0 -fno-pie -no-pie build/nocticore.c -o challenge/nocticore
```

## Security and Integration Notes

- All flags and evidence are synthetic.
- This solution is for the challenge authors, not participants.
- The 32-bit hash is a challenge verification mechanism, not cryptographic authentication. Hash collisions are possible.
- Development placeholders must be replaced or confirmed before final integration.
- Distribute only the intended participant artifact through CTFd, not the author solution or source code.
