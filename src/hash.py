from argparse import ArgumentParser

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
    print(hash.hash(args.x))