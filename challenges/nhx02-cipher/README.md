# NHX-02 – Cipher at Dusk

## Domain

Cryptography / Programming

## Difficulty

Easy

## Points

100

## Scenario

Evidence recovered from the previous stage points to a short message used by HEX-SHADOW. The message is unreadable because multiple simple transformations were applied.

## Participant Task

Analyze `dusk_message.txt`, identify the transformations, reverse them in the correct order, and recover the stage flag and evidence fragment.

## Intended Tools

- `cat`
- `base64`
- CyberChef
- Python 3
- basic string manipulation

## Intended Solution Path

1. Inspect the encoded text.
2. Notice that the character set resembles Base64.
3. Decode the Base64 layer.
4. Observe that the output is still transformed.
5. Identify the Caesar-style shift.
6. Reverse the Caesar shift.
7. Recover the flag and evidence fragment.
8. Submit the flag to CTFd.

## Hints

### Hint 1 — 5 points

Encoding and encryption are not the same thing.

### Hint 2 — 10 points

The outer layer uses a common Base64 representation.

## Reset / Recovery

This is a static-file challenge. No live reset is required. A clean copy of `dusk_message.txt` can be re-downloaded from CTFd or restored from the repository.

## Security Note

All data is fictional and created only for the NoctiHex CTF.