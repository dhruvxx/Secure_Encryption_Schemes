from argparse import ArgumentParser

PRIME = 48661
GENERATOR = 959
SEED_SIZE = 16

class PRG:
    def __init__(self):
        pass
    def binit(self, ord):
        a = bin(ord)
        b = a.replace("0b", "")
        return b
    def prg(self, seed):
        result = ""
        binary = self.binit(seed).zfill(SEED_SIZE)
        for _ in range(2 * SEED_SIZE):
            binary = (
                self.binit(pow(GENERATOR, int(binary, 2), PRIME))
                .zfill(SEED_SIZE)
            )
            result += binary[0]

        return int(result, 2)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "seed", type=int, help="The seed to use for random number generator"
    )

    # Parse arguments
    args = parser.parse_args()
    if len(bin(args.seed).replace("0b", "")) > SEED_SIZE:
        raise ValueError("'seed' has to be less than ${SEED_SIZE} bits")
    prg1 = PRG()
    print(prg1.prg(args.seed))