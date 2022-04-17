


from board import Board
import pygame
from gui import GUI
from algorithm import Algorithm

WINDOWS_SIZE = [500, 500]
DEBUG_MODE = False

class KnightsTour:
    def __init__(self, board_size:tuple, start_pos:tuple, algo_approach=None) -> None:
        self._board_size = board_size
        self._board = Board(board_size, start_pos)
        self._gui = None
        self._algo = algo_approach
        self.start()

    def _curser_debug(self, event):
        # False = can continue
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

                    # check current tile see if any legel move avaliable.
                    self._board.check_legel_move(target_pos, target_pos)
            except Board.NotSloveException:
                print("Unfortunally, You Did Not Solved The Problem!\nPath:")
                self._board.show_path()
                return False
        
        return True
    
    def _slove(self, algo):
        approach = Algorithm(self._board, algo)
        return approach.get_result()


    def start(self):
        pygame.init()
        pygame.display.set_caption('SIT-215 PBL2 KnightsTour [Group-6]')

        # Set up the drawing window
        self._gui = GUI(WINDOWS_SIZE, pygame, self._board.get_tiles())
        self._gui.set_caption('SIT-215 PBL2 KnightsTour [Group-6]')

        # Run until the user asks to quit
        running = True
        self._gui.draw_board()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if (DEBUG_MODE is True):
                    running = self._curser_debug(event)
                else:
                    solution = self._slove(self._algo)
                    if len(solution[0]) == pow(self._board.get_size(), 2):
                        # play movement
                        for move in solution[0]:
                            target_pos = {'x': move[0], 'y': move[1]}
                            self._board.move(target_pos)
                            self._gui.draw_board()
                            self._gui.draw_path(self._board.get_paths(), target_pos, self._board.get_size())
                            self._gui.refresh()
                            pygame.time.wait(1000)

                        running = False

                self._gui.refresh()

        pygame.quit()
        
