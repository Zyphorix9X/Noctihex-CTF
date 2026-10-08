# NHX-06 — NoctiCore

## Domain
Reverse Engineering / Linux ELF

## Difficulty
Hard

## Points
500

## Scenario
HEX-SHADOW has concealed the final NoctiHex incident evidence inside a Linux executable called NoctiCore.

The executable verifies evidence collected throughout the previous five challenges. Participants must analyze its verification algorithm, reconstruct the correct evidence chain, and unlock the final flag.

## Participant Task
Analyze the `nocticore` Linux ELF executable and provide the correct evidence chain to recover the final flag.

## Intended Tools
- Linux terminal
- `file`
- `strings`
- GDB or Ghidra
- Python 3

## Intended Solution Path
1. Download the NoctiCore executable.
2. Identify its Linux ELF format.
3. Inspect its strings and program behavior.
4. Reverse-engineer the custom verification algorithm.
5. Recover evidence fragments from NHX-01 through NHX-05.
6. Combine the fragments in the correct order using `|` as a separator.
7. Execute NoctiCore with the completed evidence chain.
8. Recover and submit the final flag.

## Hints

### Hint 1 — 10 points
The previous stages contain more than individual flags.

### Hint 2 — 20 points
Five fragments form one chain. Their order matters.

### Hint 3 — 30 points
The executable calculates a 32-bit verification value from its input.

## Build Instructions

From the `nhx06-nocticore` directory on Linux:

```bash
gcc -O0 -fno-pie -no-pie build/nocticore.c -o challenge/nocticore
```

## Reset / Recovery
This is a static-file challenge. No running service is required. Restore the original executable from the repository or rebuild it from the source code.

## Security Note
All artifacts, evidence fragments, and flags are synthetic and created only for the NoctiHex CTF.
