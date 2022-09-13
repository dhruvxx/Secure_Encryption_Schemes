from argparse import ArgumentParser
import base64

P = 32633
G = 275
H = pow(G, 69, P)
N = 16

class Hash:
    def __init__(self):
        pass
    def hash(self, x):
        if len(bin(x).replace("0b", "")) > 2 * N:
            raise ValueError(f"'x' should be less than {2*N} bits")

        # Split into two halfs
        x1 = x >> N
        x1 = x1 & 0xFF
        x2 = x & 0xFF

        # Generate hash
        y = (pow(G, x1, P) * pow(H, x2, P)) % P

        return y

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("x", type=int, help="the integer to hash")

    # Parse arguments
    args = parser.parse_args()
    hash = Hash()

BLOCK_SIZE = 16
IV = 10007

hash = Hash()

class MDT:
    def __init__(self):
        pass
    def mdt(self, message):
        if len(message) > 2 ** BLOCK_SIZE - 1:
            raise ValueError(
                "length of 'message' has to be less than ${(2**BLOCK_SIZE - 1)}"
            )
        result = IV
        for i in range(0, len(message), BLOCK_SIZE // 8):
            # Get binary representation of message
            bitstring = ""
            for j in range(BLOCK_SIZE // 8):
                if i + j < len(message):
                    bitstring += bin(message[i + j]).replace("0b", "").zfill(8)
                else:
                    bitstring += "0" * 8

            result = result + (int(bitstring, 2) << BLOCK_SIZE)
            result = hash.hash(result)

        # Append length of message
        result = result + (len(message) << BLOCK_SIZE)
        result = hash.hash(result)

        return base64.b64encode(result.to_bytes(BLOCK_SIZE // 8, "big")).decode("utf8")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("message", type=str, help="the message to hash")

    # Parse arguments
    args = parser.parse_args()
    mdt = MDT()
    print(mdt.mdt(str.encode(args.message)))