# NHX-01 – Whispers in the Static

## Domain

Steganography / File and Metadata Analysis

## Difficulty

Easy

## Points

100

## Scenario

A suspicious PNG image was recovered from the fictional NoctiHex Labs incident. Although the image appears ordinary, the incident response team believes HEX-SHADOW concealed additional evidence inside it.

## Participant Task

Investigate `midnight_signal.png` and recover the stage flag and evidence fragment.

## Intended Tools

- `file`
- ExifTool
- `unzip`
- `strings`
- archive/file inspection utilities

## Intended Solution Path

1. Verify the file type.
2. Inspect the PNG metadata.
3. Notice the clue referring to embedded file structures.
4. Inspect the image for appended archive data.
5. Extract `evidence.txt`.
6. Recover the flag and evidence fragment.
7. Submit the flag to CTFd.

## Hints

### Hint 1 — 5 points

An image can contain information that is not visible.

### Hint 2 — 10 points

Inspect both metadata and embedded file structures.

## Reset / Recovery

This is a static-file challenge. No live reset is required. A clean copy of `midnight_signal.png` can be downloaded again from CTFd or restored from the repository.

## Security Note

All content is synthetic and was created specifically for the NoctiHex CTF.