import base64
from argparse import ArgumentParser
from mdt import *
from hash import *

BLOCK_SIZE = 16
OPAD = 0x36
IPAD = 0x5C
mdt = MDT()
hash = Hash()
class HMAC:
    def __init__(self):
        pass

    def generate_hmac(self, message, key):
        if len(bin(key).replace("0b", "")) > BLOCK_SIZE:
            raise ValueError(f"'key' has to be less than ${BLOCK_SIZE} bits")

        ikey = key
        okey = key
        step = BLOCK_SIZE // 16
        for i in range(step):
            ikey = ikey ^ (IPAD << (i * 16))
            okey = okey ^ (OPAD << (i * 16))
        step = BLOCK_SIZE // 8
        inter = mdt.mdt(ikey.to_bytes(step, "big") + message)
        inter = int.from_bytes(base64.b64decode(inter), "big")

        hmac = hash.hash(IV + (okey << BLOCK_SIZE))
        hmac = hash.hash(hmac + (inter << BLOCK_SIZE))

        return base64.b64encode(hmac.to_bytes(step, "big")).decode("utf8")


    def verify_hmac(self, message, hmac, key):
        return self.generate_hmac(message, key) == hmac


if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Arguments for generate mode
    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument(
        "message", type=str, help="the message to generate HMAC for"
    )
    generate_parser.add_argument("key", type=int, help="the key to use for generation")

    # Arguments for verify mode
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument(
        "message", type=str, help="the message to verify HMAC for"
    )
    verify_parser.add_argument("key", type=int, help="the key to use for verification")
    verify_parser.add_argument("hmac", type=str, help="the HMAC to verify against")

    # Parse arguments
    args = parser.parse_args()
    hmac = HMAC()
    if args.mode == "generate":
        print(hmac.generate_hmac(str.encode(args.message), args.key))
    else:
        print(hmac.verify_hmac(str.encode(args.message), args.hmac, args.key))