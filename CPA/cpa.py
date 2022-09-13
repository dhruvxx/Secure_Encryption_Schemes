import base64
from argparse import ArgumentParser
from tracemalloc import start
from prf import *

prf = PRF()

KEY_SIZE = 16

class CPA:
    def __init__(self):
        pass
    
    def binit(self, ord):
        a = bin(ord)
        b = a.replace("0b", "")
        return b
        
    def cpa_encrypt(self, message, key, start_ctr):
        binner_key = bin(key)
        binner_key.replace("0b", "")
        binner_ctr = bin(start_ctr)
        binner_ctr = binner_ctr.replace("0b", "")
        if len(binner_key) > KEY_SIZE:
            raise ValueError(f"'key' has to be less than ${KEY_SIZE} bits")
        if len(binner_ctr) > KEY_SIZE:
            raise ValueError(f"'start_ctr' has to be less than ${KEY_SIZE} bits")
        ctr = start_ctr
        final_string = start_ctr.to_bytes(KEY_SIZE // 8, "big")
        steps = KEY_SIZE // 8
        for i in range(0, len(message), steps):
            # Get binary representation of message
            bitstring = ""
            for j in range(steps):
                if i + j < len(message):
                    bitstring += self.binit(ord(message[i + j])).zfill(8)
                else:
                    bitstring += "0" * 8

            # Encrypt
            m = int(bitstring, 2)
            c = m ^ prf.prf(ctr, key)

            # Convert back to ascii representation
            final_string += c.to_bytes(steps, "big")
            ctr += 1

        # Encode result as a base64 string
        cipher = base64.b64encode(final_string).decode("utf8")
        return cipher


    def cpa_decrypt(self, cipher, key):
        if len(bin(key).replace("0b", "")) > KEY_SIZE:
            raise ValueError("'key' has to be less that ${KEY_SIZE} bits")

        binary_string = base64.b64decode(cipher)
        ctr = int.from_bytes(binary_string[: KEY_SIZE // 8], "big")
        binary_string = binary_string[KEY_SIZE // 8 :]
        final_string = ""
        steps=KEY_SIZE // 8
        for i in range(0, len(binary_string), steps):
            # Get binary representation of ciphertext
            bitstring = ""
            for j in range(steps):
                bitstring += self.binit(binary_string[i + j]).zfill(8)

            # Decrypt
            c = int(bitstring, 2)
            m = c ^ prf.prf(ctr, key)

            # Convert back to ascii
            for j in range(steps - 1, -1, -1):
                final_string += chr((m >> j * 8) & 0xFF)

            ctr += 1

        return final_string


if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Arguments for generate mode
    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("message", type=str, help="the message to encrypt")
    encrypt_parser.add_argument("key", type=int, help="the key to use for encrytion")
    encrypt_parser.add_argument(
        "--ctr",
        type=int,
        default=420,
        help="start counter to use for randomized counter mode",
    )

    # Arguments for verify mode
    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("cipher", type=str, help="the cipher to decrypt")
    decrypt_parser.add_argument("key", type=int, help="the key to use for decryption")

    # Parse arguments
    args = parser.parse_args()
    cpa = CPA()
    if args.mode == "encrypt":
        print(cpa.cpa_encrypt(args.message, args.key, args.ctr))
    else:
        print(cpa.cpa_decrypt(args.cipher, args.key))