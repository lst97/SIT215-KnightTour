from knightstour import KnightsTour
from algorithm import Algorithm

BOARD_SIZE = (5, 5)
START_POS = {'x': 0, 'y': 0}

def main():
    approach = Algorithm.BT # replace with different approach algorithm
    KnightsTour(BOARD_SIZE, START_POS, approach)

main()
