# NHX-04 – Packet After Midnight

## Category
Networking / Digital Forensics

## Difficulty
Moderate

## Points
200

## Description
A synthetic packet capture contains several fictional network
conversations. Participants must analyze the traffic and identify
the suspicious communication associated with HEX-SHADOW.

## Challenge File
challenge/midnight_traffic.pcap

## Intended Tools
- Wireshark

## Intended Solution Path

1. Open the PCAP in Wireshark.
2. Inspect network conversations.
3. Identify HTTP/TCP traffic.
4. Locate the suspicious /sync request.
5. Follow the relevant TCP stream.
6. Recover the evidence fragment and stage flag.

## Evidence Fragment

DEV_E4

## Development Flag

NOCTIHEX{DEV_NHX04}

## Hints

### Hint 1
Start with Statistics and Conversations instead of inspecting
every packet manually.

### Hint 2
Look for unusual HTTP paths and identify the suspicious host.

## Reset

NHX-04 is a static challenge.

Reset is performed by replacing the challenge PCAP with the
original generated file.

The PCAP can also be regenerated using:

python generate_nhx04.py

## Safety

All traffic in this challenge is synthetically generated.
No institutional, public, or personal network traffic is captured.