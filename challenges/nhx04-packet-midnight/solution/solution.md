# NHX-04 Intended Solution

1. Open midnight_traffic.pcap using Wireshark.

2. Review:
   Statistics → Conversations

3. Apply the display filter:

   http

4. Inspect the HTTP requests.

5. Locate the request:

   /sync

6. Select the packet.

7. Right-click:
   Follow → TCP Stream

8. The stream contains:

   agent=HEX-SHADOW
   fragment=DEV_E4
   flag=NOCTIHEX{DEV_NHX04}

9. Submit the recovered flag to CTFd.

## Expected Evidence

DEV_E4
