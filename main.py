from knightstour import KnightsTour
from algorithm import Algorithm

BOARD_SIZE = (12, 12)
START_POS = {'x': 0, 'y': 0}

def main():
    approach = Algorithm.Warnsdorff # replace with different approach algorithm
    KnightsTour(BOARD_SIZE, START_POS, approach)

main()
