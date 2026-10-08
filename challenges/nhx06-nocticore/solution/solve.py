import sys


def rotl32(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def nocti_check(text):
    acc = 0x3132

    for i, byte in enumerate(text.encode("utf-8")):
        acc = rotl32(acc, 5) ^ byte
        acc = (acc + i * 17) & 0xFFFFFFFF

    return acc


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 solve.py "E1|E2|E3|E4|E5"')
        sys.exit(1)

    result = nocti_check(sys.argv[1])
    print(f"Derived check: 0x{result:08x}")

    if result == 0xDC071061:
        print("Evidence chain matches the development verifier.")
    else:
        print("Evidence chain does not match.")


if __name__ == "__main__":
    main()
    