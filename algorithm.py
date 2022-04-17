
import numpy as np
class Algorithm():
    class BT():
        # Backtracking
        def __init__(self, board_size, sloved_pool=[]) -> None:
            self._possible_x = (2, 1, -1, -2, -2, -1, 1, 2)
            self._possible_y = (1, 2, 2, 1, -1, -2, -2, -1)
            self._sloved_pool = sloved_pool # for different results
            self._board_size = board_size
            self._board = []

        def validate_move(self, bo, row, col):
            if row < self._board_size and row >= 0 and col < self._board_size and col >= 0 and bo[row][col] == 0:
                return True

        def solve (self, board, row, col, n, counter):
            for i in range(len(self._possible_x)):
                if counter >= n * n + 1:
                    self._board = board
                    self._sloved_pool.append([])
                    return True

                new_x = row + self._possible_x[i]
                new_y = col + self._possible_y[i]
                if self.validate_move(board, new_x, new_y):
                    board[new_x,new_y] = counter
                    if self.solve(board,new_x, new_y, n, counter+1):
                        self._sloved_pool[len(self._sloved_pool) - 1].append([new_y, new_x])
                        return True
                    board[new_x,new_y] = 0
            return False
            
    class BFS():
        def __init__(self) -> None:
            pass
            
    class DFS():
        def __init__(self) -> None:
            pass

    def __init__(self, main_board, algo) -> None:
        self._paths = main_board.get_paths()
        self._algo = algo(main_board.get_size())
        self._board = np.zeros((main_board.get_size(), main_board.get_size()))

    def get_result(self):
        path_log = []
        path_log.append(self._paths[:])
        self._board[self._paths[0][1], self._paths[0][0]] = 1
        self._algo.solve(self._board,self._paths[0][1],self._paths[0][0],len(self._board),2)
        self._algo._sloved_pool[0].append([self._paths[0][1], self._paths[0][0]]) # change the index if multiple reuslt accure
        self._algo._sloved_pool[0] = self._algo._sloved_pool[0][::-1]
        return self._algo._sloved_pool