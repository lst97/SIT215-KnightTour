

from tile import Tile

LIGHT_COLOR = (0, 0, 0) # White
DARK_COLOR = (255, 255, 255) # Black

class Board:
    class NotSloveException(Exception):
        """ Class for custom exceptions"""
        pass

    def __init__(self, size:tuple, start_pos={'x': 0, 'y': 0}) -> None:
        if(size[0] != size[1]):
            raise Exception("Not a Square Board")
        
        self._size = size
        self._tiles = self.make_tiles()
        self._current_pos = start_pos
        self._current_step = 1
        self._path_log = []
        self.get_tile(start_pos['x'], start_pos['y']).set_status(True)
        self._path_log.append([start_pos['x'], start_pos['y']])

    def get_tiles(self):
        return self._tiles
    
    def get_tile(self, x, y):
        return self.get_tiles()[x][y]

    def get_mouse_tile_pos(self, pos:tuple, screen_size:list):
        tile_pos_x = tile_pos_y = 0
        offset = int(screen_size[0] / self.get_size())
        
        x_found = y_found = False
        
        for i in range(self.get_size()):
            if(x_found == False):
                if(pos[0] > offset * i and pos[0] < offset * (i + 1)):
                    tile_pos_x = i
                    x_found = True

            if(y_found == False):
                if(pos[1] > offset * i and pos[1] < offset * (i + 1)):
                    tile_pos_y = i
                    y_found = True
        
        return tile_pos_x, tile_pos_y

    def get_step_count(self):
        return self._current_step

    def get_paths(self):
        return self._path_log

    def show_path(self):
        print(self._path_log)

    def move(self, target_pos:dict):
        target_tile = self.get_tile(target_pos['x'], target_pos['y'])
        if (self.check_legel_move(self._current_pos, target_pos) is True and target_tile.is_visited() == False):
            target_tile.set_status(True)
            target_tile.set_step(self._current_step + 1)

            self._current_step += 1
            self._current_pos = target_pos

            self._path_log.append([target_pos['y'], target_pos['x']])
            return True
        return False

    def check_legel_move(self, current_pos:dict, target_pos:dict):
        legel_moves = []
        board_edge = self.get_size()
        
        # find legel pos for current_pos
        # can be optimzied?
        if (current_pos['x'] + 2 < board_edge):
            if(current_pos['y'] + 1 < board_edge):
                # tile that already moved not count as legel
                target_tile = self.get_tile(current_pos['x'] + 2, current_pos['y'] + 1)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] + 2, current_pos['y'] + 1])
            if(current_pos['y'] - 1 > -1):
                target_tile = self.get_tile(current_pos['x'] + 2, current_pos['y'] - 1)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] + 2, current_pos['y'] - 1])
        if (current_pos['x'] - 2 > -1):
            if(current_pos['y'] + 1 < board_edge):
                target_tile = self.get_tile(current_pos['x'] - 2, current_pos['y'] + 1)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] - 2, current_pos['y'] + 1])
            if(current_pos['y'] - 1 > -1):
                target_tile = self.get_tile(current_pos['x'] - 2, current_pos['y'] - 1)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] - 2, current_pos['y'] - 1])
        if (current_pos['y'] + 2 < board_edge):
            if(current_pos['x'] + 1 < board_edge):
                target_tile = self.get_tile(current_pos['x'] + 1, current_pos['y'] + 2)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] + 1, current_pos['y'] + 2])
            if(current_pos['x'] - 1 > -1):
                target_tile = self.get_tile(current_pos['x'] - 1, current_pos['y'] + 2)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] - 1, current_pos['y'] + 2])
        if (current_pos['y'] - 2 > -1):
            if(current_pos['x'] + 1 < board_edge):
                target_tile = self.get_tile(current_pos['x'] + 1, current_pos['y'] - 2)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] + 1, current_pos['y'] - 2])
            if(current_pos['x'] - 1 > -1):
                target_tile = self.get_tile(current_pos['x'] - 1, current_pos['y'] - 2)
                if(target_tile.is_visited() is False):
                    legel_moves.append([current_pos['x'] - 1, current_pos['y'] - 2])
        
        if len(legel_moves) == 0:
            raise Board.NotSloveException("No Legel Move!") 

        target_move = []
        for _, i in target_pos.items():
            target_move.append(i)

        is_legel = False
        for move in legel_moves:
            if(move == target_move):
                is_legel = True
                break
        
        return is_legel

    def get_size(self):
        return self._size[0]

    def get_current_pos(self):
        return self._current_pos

    def set_current_pos(self, pos):
        self._current_pos = pos

    def make_tiles(self):
        tiles = list()

        for y in range(self._size[0]):
            tiles.append([])
            for x in range(self._size[1]):
                tiles[y].append(Tile({'x': x, 'y': y}, DARK_COLOR if abs(x - y) % 2 == 0 else LIGHT_COLOR))
        
        return tiles
