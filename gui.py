
import pygame
from board import Board

LINE_COLOR = (255, 0, 0) # Red
WAIT_TIME = 100
class GUI:
    def __init__(self, size:list, pg:pygame, tiles) -> None:
        self._tiles = tiles
        self._size = size
        self._rect = pg.Rect
        self._display = pg.display
        self._draw = pg.draw
        self._time = pg.time
        self._screen = self._display.set_mode(size)
        self.refresh()
    
    def fill(self, rgb:tuple):
        self._screen.fill(rgb)
    
    def draw_path(self, pos_chain:list, target_pos:dict, board_size:int):
        # get center point of the tile
        offset = int(self._size[0] / board_size)

        previous_pos = []
        previous_pos.append(int(offset * pos_chain[0][1] + offset / 2))
        previous_pos.append(int(offset * pos_chain[0][0] + offset / 2))

        for pos in pos_chain:
            pos = [int(offset * pos[1] + offset / 2), int(offset * pos[0] + offset / 2)]
            self._draw.line(self._screen, LINE_COLOR, previous_pos, pos)
            previous_pos = pos

        target_center = []
        target_center.append(int(offset * target_pos['x'] + offset / 2))
        target_center.append(int(offset * target_pos['y'] + offset / 2))

        self._draw.line(self._screen, LINE_COLOR, previous_pos, target_center)

    def draw_paths(self, board, solutions):
        for solution in solutions:
            first_move = True
            for move in solution:
                if first_move is True :
                    # ignore first move
                    first_move = False
                    continue

                target_pos = {'x': move[0], 'y': move[1]}
                if board.move(target_pos) is True:
                    self.draw_board()
                    self.draw_path(board.get_paths(), target_pos, board.get_size())
                    self.refresh()
                    self._time.wait(WAIT_TIME)
                else:
                    raise Board.InvalidMoveException("Please Check Your Algorithm!") 

    def set_caption(self, name):
        self._display.set_caption(name)

    def draw_board(self):
        w, _ = self._display.get_surface().get_size()

        rect_width = int(w / len(self._tiles))

        board_size = len(self._tiles)
        for column in range(board_size):
            for row in range(board_size):
                color = self._tiles[column][row].get_color()

                self._draw.rect(self._screen, color, self._rect(rect_width * column, rect_width * row, rect_width, rect_width))

    def refresh(self):
        self._display.flip()
