
from board import Board
import pygame
from gui import GUI

WINDOWS_SIZE = [500, 500]
class KnightsTour:
    def __init__(self, board_size:tuple, start_pos:tuple, algo_approach) -> None:
        self._board_size = board_size
        self._board = Board(board_size, start_pos)
        self.start()

    def start(self):
        pygame.init()
        pygame.display.set_caption('SIT-215 PBL2 KnightsTour [Group-6]')

        # Set up the drawing window
        self._gui = GUI(WINDOWS_SIZE, pygame, self._board.get_tiles())
        self._gui.set_caption('SIT-215 PBL2 KnightsTour [Group-6]')

        # Run until the user asks to quit
        running = True
        pause = False
        self._gui.draw_board()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if(self._board.get_step_count() == self._board.get_size() * self._board.get_size()):
                    pause = True
                    self._gui.set_caption('Congratulation, You Solved The Problem!')
                    print("Congratulation, You Solved The Problem!\nPath:")
                    self._board.show_path()

                if event.type == pygame.MOUSEBUTTONUP and pause is False:
                    mouse_pos = pygame.mouse.get_pos()
                    x, y = self._board.get_mouse_tile_pos(mouse_pos, WINDOWS_SIZE)
                    target_pos = {'x': x, 'y': y}

                    try:
                        if (self._board.move(target_pos) is True):
                            self._gui.draw_board()
                            self._gui.draw_path(self._board.get_path(), target_pos, self._board_size)

                            # check current tile see if any legel move avaliable.
                            self._board.check_legel_move(target_pos, target_pos)
                    except Board.NotSloveException:
                        print("Unfortunally, You Did Not Solved The Problem!\nPath:")
                        self._board.show_path()

                self._gui.refresh()

        pygame.quit()
        