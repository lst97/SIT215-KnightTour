from board import Board
import pygame
from gui import GUI
from algorithm import KTAlgorithm

WINDOWS_SIZE = [500, 500]
DEBUG_MODE = False

class KnightsTour:
    def __init__(self, board_size:tuple, start_pos:tuple, algo_approach=None) -> None:
        self._board_size = board_size
        self._board = Board(board_size, start_pos)
        self._gui = GUI(WINDOWS_SIZE, pygame, self._board.get_tiles())
        self._algo = algo_approach
        self.start()

    def _curser_debug(self, event:pygame.event) -> bool:
        """Reutnr if the GUI continue to run or not

        Args:
            event (pygame.event): pygame event

        Returns:
            bool: True to keep running, else False
        """
        if(self._board.get_step_count() == pow(self._board.get_size(), 2)):
            self._gui.set_caption('Congratulation, You Solved The Problem!')
            print("Congratulation, You Solved The Problem!\nPath:")
            self._board.show_path()
            return False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            x, y = self._board.get_mouse_tile_pos(mouse_pos, WINDOWS_SIZE)
            target_pos = {'x': x, 'y': y}

            try:
                if (self._board.move(target_pos) is True):
                    self._gui.draw_board()
                    self._gui.draw_path(self._board.get_paths(), target_pos, self._board.get_size())

                    # check current tile see if any legal move avaliable.
                    self._board.check_legal_move(target_pos, target_pos)
            except Board.NoSloveException:
                print("Unfortunally, Those Moves Cant Solved The Problem!\nPath:")
                self._board.show_path()
                return False
        
        return True
    
    def _slove(self, algo) -> list:
        """Driver function

        Args:
            algo (Any): Either BT, ANN or Warnsdorff

        Returns:
            list: solution paths
        """
        approach = KTAlgorithm(self._board, algo)
        try:
            return approach.get_result()
        except KTAlgorithm.NoSolutionException:
            return list()

    def start(self):
        """Start the GUI for KT visulization
        """
        pygame.init()
        self._gui.set_caption('SIT-215 PBL2 KnightsTour [Group-6]')

        running = True
        self._gui.draw_board()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                if (DEBUG_MODE is True):
                    # using cursor
                    running = self._curser_debug(event)
                else:
                    # using algorithm
                    solutions = self._slove(self._algo)
                    if len(solutions) != 0:
                        print("{} solution(s) found!".format(len(solutions)))
                        print(solutions)
                        # play moves
                        self._gui.draw_paths(self._board, solutions)
                    else:
                        print("No Solution!")
                    running = False
                    break
                self._gui.refresh()
        input("Press any key to exit.")
        pygame.quit()
        
