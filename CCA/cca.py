from argparse import ArgumentParser
from mac import *
from cpa import *

KEY_SIZE = 16
cpa = CPA()
mac = MAC()
class Crypt:

    def __init__(self):
        pass
    def cca_encrypt(self, message, key1, key2, start_ctr):
        # Check if key1 and key2 are same
        if key1 == key2:
            raise ValueError("'key1' and 'key2' should not be the same")
        cipher = cpa.cpa_encrypt(message, key1, start_ctr)
        return cipher, mac.generate_mac(cipher, key2)
    def cca_decrypt(self, cipher, key1, key2, macval):
        if macval != mac.generate_mac(cipher, key2):
            raise ValueError("MAC verification failed")
        return cpa.cpa_decrypt(cipher, key1)
    
    
if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Arguments for generate mode
    encrypt_parser = subparsers.add_parser("encrypt")
    encrypt_parser.add_argument("message", type=str, help="the message to encrypt")
    encrypt_parser.add_argument("key1", type=int, help="the key to use for encrytion")
    encrypt_parser.add_argument(
        "key2", type=int, help="the key to use for generating MAC"
    )
    encrypt_parser.add_argument(
        "--ctr",
        type=int,
        default=420,
        help="start counter to use for randomized counter mode",
    )

    # Arguments for verify mode
    decrypt_parser = subparsers.add_parser("decrypt")
    decrypt_parser.add_argument("cipher", type=str, help="the message to encrypt")
    decrypt_parser.add_argument("key1", type=int, help="the key to use for decryption")
    decrypt_parser.add_argument(
        "key2", type=int, help="the key to use for verifying MAC"
    )
    decrypt_parser.add_argument("mac", type=str, help="the MAC to verify against")

    # Parse arguments
    args = parser.parse_args()
    cryptor = Crypt()
    if args.mode == "encrypt":
        print(cryptor.cca_encrypt(args.message, args.key1, args.key2, args.ctr))
    else:
        print(cryptor.cca_decrypt(args.cipher, args.key1, args.key2, args.mac))
