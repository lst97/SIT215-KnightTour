from knightstour import KnightsTour
from algorithm import KTAlgorithm

BOARD_SIZE = (6, 6)
START_POS = {"x": 0, "y": 0}


def main():
    approach = KTAlgorithm.Warnsdorff  # replace with different algorithm
    KnightsTour(BOARD_SIZE, START_POS, approach)


main()
