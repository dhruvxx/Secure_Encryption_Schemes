import base64
from math import ceil
from argparse import ArgumentParser
from prf import *
prf = PRF()

KEY_SIZE = 16

class MAC:
    def __init__(self):
        pass

    def verify_mac(self, message, mac, key):
        return mac == self.generate_mac(message, key)

    def generate_mac(self, message, key):
        if len(bin(key).replace("0b", "")) > KEY_SIZE:
            raise ValueError(f"'key' has to be less that ${KEY_SIZE} bits")

        if 8 * len(message) > (2 ** KEY_SIZE - 1) * KEY_SIZE:
            raise ValueError(
                f"length of 'message' has to be less that ${(2**KEY_SIZE - 1)*KEY_SIZE}"
            )

        # Initialization vector is PRF(l, key) in variable length CBC-MAC
        l = ceil(len(message) / KEY_SIZE)
        mac = prf.prf(l, key)

        for i in range(0, len(message), KEY_SIZE // 8):
            # Get binary representation of message
            bitstring = ""
            for j in range(KEY_SIZE // 8):
                if i + j < len(message):
                    bitstring += bin(ord(message[i + j])).replace("0b", "").zfill(8)
                else:
                    bitstring += "0" * 8

            # Generate block MAC
            mac = prf.prf(int(bitstring, 2) ^ mac, key)

        return base64.b64encode(mac.to_bytes(KEY_SIZE // 8, "big")).decode("utf8")


if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Arguments for generate mode
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument(
        "message", type=str, help="the message to generate MAC for"
    )
    generate_parser.add_argument("key", type=int, help="the key to use for generation")

    # Arguments for verify mode
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument(
        "message", type=str, help="the message to verify MAC for"
    )
    verify_parser.add_argument("key", type=int, help="the key to use for verification")
    verify_parser.add_argument("mac", type=str, help="the MAC to verify against")

    # Parse arguments
    args = parser.parse_args()
    mac = MAC()
    if args.mode == "generate":
        print(mac.generate_mac(args.message, args.key))
    else:
        print(mac.verify_mac(args.message, args.mac, args.key))