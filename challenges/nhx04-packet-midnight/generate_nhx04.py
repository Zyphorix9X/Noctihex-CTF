from scapy.all import IP, TCP, Raw, wrpcap

packets = []

def add_http(src, dst, sport, path, body=""):
    request = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: noctihex.local\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"\r\n"
        f"{body}"
    )

    packet = (
        IP(src=src, dst=dst) /
        TCP(sport=sport, dport=80, flags="PA") /
        Raw(load=request.encode())
    )

    packets.append(packet)


# Decoy traffic
add_http(
    "10.13.37.10",
    "10.13.37.20",
    41001,
    "/health",
    "status=ok"
)

add_http(
    "10.13.37.11",
    "10.13.37.20",
    41002,
    "/archive",
    "archive=empty"
)

# Important challenge traffic
add_http(
    "10.13.37.50",
    "10.13.37.20",
    41003,
    "/sync",
    "agent=HEX-SHADOW&fragment=DEV_E4&flag=NOCTIHEX{DEV_NHX04}"
)

wrpcap(
    "challenge/midnight_traffic.pcap",
    packets
)

print("[+] Generated synthetic capture")
print(f"[+] Packets: {len(packets)}")
print("[+] Output: challenge/midnight_traffic.pcap")