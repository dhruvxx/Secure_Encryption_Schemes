from argparse import ArgumentParser
from prg import *

SEED_SIZE = 16
prg1 = PRG()

class PRF:
    def __init__(self):
        pass
    def prf(self, r, seed):
        binary_r = bin(r).replace("0b", "").zfill(SEED_SIZE)
        new_seed = seed
        for i in range(SEED_SIZE):
            result = prg1.prg(new_seed)
            new_seed = bin(result).replace("0b", "").zfill(SEED_SIZE)
            if binary_r[SEED_SIZE - i - 1] == "0":
                new_seed = new_seed[:SEED_SIZE]
            else:
                new_seed = new_seed[SEED_SIZE:]

            new_seed = int(new_seed, 2)
        return new_seed


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("r", type=int, help="The input to PRF")
    parser.add_argument(
        "seed", type=int, help="The seed to use for random number generator"
    )

    # Parse arguments
    args = parser.parse_args()

    if len(bin(args.r).replace("0b", "")) > SEED_SIZE:
        raise ValueError("'r' has to be less that ${SEED_SIZE} bits")

    if len(bin(args.seed).replace("0b", "")) > SEED_SIZE:
        raise ValueError("'seed' has to be less that ${SEED_SIZE} bits")
    prfit = PRF()
    print(prfit.prf(args.r, args.seed))