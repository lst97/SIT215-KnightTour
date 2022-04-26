import random as rnd # Warnsdorff

class Algorithm():
    class NoSolutionException(Exception):
        """ Class for custom exceptions"""
        pass

    class BT():
        # Backtracking
        def __init__(self, board_size, current_pos=None, sloved_pool=[]) -> None:
            print("Searching for solution using BackTracking...")
            # TODO show each path that BT tried in GUI and different solution.
            self._possible_x = (2, 1, -1, -2, -2, -1, 1, 2)
            self._possible_y = (1, 2, 2, 1, -1, -2, -2, -1)
            self._sloved_pool = sloved_pool # for different results
            self._board_size = board_size
            self._board = []

            for i in range(board_size):
                self._board.append([])
                for _ in range(board_size):
                    self._board[i].append(0)

            self._board[current_pos['y']][current_pos['x']] = 1

        def _validate_move(self, x, y):
            return True if x < self._board_size and x >= 0 and y < self._board_size and y >= 0 and self._board[y][x] == 0 else False

        def solve (self, row, col, counter):
            for i in range(len(self._possible_x)):
                if counter >= pow(self._board_size, 2) + 1:
                    self._sloved_pool.append([])
                    return True

                new_x = row + self._possible_x[i]
                new_y = col + self._possible_y[i]
                if self._validate_move(new_x, new_y):
                    self._board[new_y][new_x] = counter
                    if self.solve(new_x, new_y, counter + 1):
                        self._sloved_pool[len(self._sloved_pool) - 1].append([new_x, new_y])
                        return True

                    self._board[new_y][new_x] = 0
            return False
            
    class Warnsdorff():
        # Warnsdorff's Algorithm
        def __init__(self, board_size, _=None, sloved_pool=[]) -> None:
            self._board_size = board_size
            self._possible_x = (2, 1, -1, -2, -2, -1, 1, 2)
            self._possible_y = (1, 2, 2, 1, -1, -2, -2, -1)
            self._sloved_pool = sloved_pool
            self._solution_moves = []
            self._board_size = board_size
            self._board = []
            self._next_step = -1
            self._rand = rnd
            
            for i in range(board_size):
                self._board.append([])
                for _ in range(board_size):
                    self._board[i].append(0)
        
        def _validate_move(self, x, y):
            return True if x < self._board_size and x >= 0 and y < self._board_size and y >= 0 and self._board[y][x] == 0 else False

        def solve(self, row, col, counter):
            # place knight
            self._next_step += counter
            self._solution_moves.append([row, col])
            self._board[row][col] = self._next_step
            self._next_step += 1

            for i in range(pow(self._board_size, 2)):
                step_count = self._next_move({'x': self._solution_moves[i][1], 'y': self._solution_moves[i][0]})
                if (step_count is None and self._next_step < pow(self._board_size, 2)):
                    return False
            
            # close tour
            if (self._solution_moves[-1] == self._solution_moves[0]):
                self._solution_moves.pop()

            self._sloved_pool.append(self._solution_moves)
            return True

        def _is_empty(self, row, col):
            return (self._validate_move(row, col)) and (self._board[col][row] == 0);

        def _get_degree(self, row, col):
            count = 0
            for i in range(len(self._possible_x)):
                if(self._is_empty(row + self._possible_y[i], col + self._possible_x[i])):
                    count += 1
            return count
        
        # Warnsdorff's heuristic
        def _next_move(self, pos:dict):
            possible_move = len(self._possible_x)
            degree_count = None
            min_deg_index = -1
            min_deg = possible_move
            next_x = None
            next_y = None

            # Try all N adjacent starting
            # from random adjacent then find
            # minium degree.
            rand_i = self._rand.randint(0, possible_move + 1)
            for count in range(possible_move):
                i = (rand_i + count) % possible_move
                next_x = pos['x'] + self._possible_x[i]
                next_y = pos['y'] + self._possible_y[i]
                degree_count = self._get_degree(next_y, next_x)
                if(self._is_empty(next_y, next_x) and degree_count < min_deg):
                    min_deg_index = i
                    min_deg = degree_count
            
            if (min_deg_index == -1):
                return None

            next_x = pos['x'] + self._possible_x[min_deg_index]
            next_y = pos['y'] + self._possible_y[min_deg_index]

            self._solution_moves.append([next_y, next_x])
            self._board[next_x][next_y] = self._next_step
            self._next_step += 1
            return len(self._solution_moves)
    
    # class DFS():
    #     def __init__(self) -> None:
    #         pass

    def __init__(self, main_board, algo) -> None:
        self._paths = main_board.get_paths()
        self._algo = algo(main_board.get_size(), main_board.get_current_pos())

    def get_result(self):
        path_log = []
        path_log.append(self._paths[:])
        self._algo.solve(self._paths[0][1], self._paths[0][0], 2)
        if len(self._algo._sloved_pool) != 0:
            if self._algo is self.BT:
                self._algo._sloved_pool[0].append([self._paths[0][1], self._paths[0][0]]) # change the index if multiple reuslt accure
                self._algo._sloved_pool[0] = self._algo._sloved_pool[0][::-1] # reverse order due to recursion.
        else:
            raise self.NoSolutionException() 
        return self._algo._sloved_pool
