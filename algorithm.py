import random as rnd  # Warnsdorff
import numpy as np  # ANN
import numpy.random as nprnd  # ANN

from board import Board

MAX_ITERATION = 25  # maximum iteration for ANN

POSSIBLE_X = (2, 1, -1, -2, -2, -1, 1, 2)
POSSIBLE_Y = (1, 2, 2, 1, -1, -2, -2, -1)


class KTAlgorithm:
    """
    Board data x indicate verticle posistion,
    y indicate horizontal posistion.

    Raises:
        self.NoSolutionException: raise it if all possible move tried and still no solution.

    """

    @staticmethod
    def _validate_move(board: list, col: int, row: int) -> bool:
        """Validate if the possible move is valid

        Args:
            board (list): Board data
            col (int): row
            row (int): column

        Returns:
            int: True if the posistion is a valid move, else False.
        """
        return (
            True
            if (
                0 <= col < len(board) and 0 <= row < len(board) and board[row][col] == 0
            )
            else False
        )

    @staticmethod
    def _init_board(board_size: int) -> list:
        """init board to 0

        Args:
            board_size (int): square size of the board
        """
        board = []
        # init board to all zero.
        for i in range(board_size):
            board.append([])
            for _ in range(board_size):
                board[i].append(0)
        return board

    class NoSolutionException(Exception):
        """All possible move tried and still no solution."""

        pass

    class BT:
        """Find one solution using Backtracking Algorithm"""

        # Backtracking Algorithm
        def __init__(self, board_size: int, sloved_pool=[]) -> None:
            print("Searching for solution using BackTracking Algorithm...")

            self._sloved_pool = sloved_pool  # for different results, only one for now
            self._board_size = board_size
            self._board = []

            # init board to all zero.
            self._board = KTAlgorithm._init_board(self._board_size)

        def solve(self, col: int, row: int, counter: int = None) -> bool:
            # first move
            if counter == 1:
                self._board[row][col] = 1
                counter += 1

            for i in range(len(POSSIBLE_X)):
                if counter >= pow(self._board_size, 2) + 1:
                    # solution found
                    self._sloved_pool.append([])
                    return True

                new_x = col + POSSIBLE_X[i]
                new_y = row + POSSIBLE_Y[i]
                if KTAlgorithm._validate_move(self._board, new_x, new_y):
                    self._board[new_y][new_x] = counter
                    if self.solve(new_x, new_y, counter + 1):
                        self._sloved_pool[len(self._sloved_pool) - 1].append(
                            # add path in reversed order due to recursion.
                            [new_x, new_y]
                        )
                        return True

                    self._board[new_y][new_x] = 0
            return False

    class Warnsdorff:
        # Warnsdorff's Algorithm
        def __init__(self, board_size: int, sloved_pool: list = []) -> None:
            print("Searching for solution using Warnsdorff's Algorithm...")

            self._board_size = board_size
            self._sloved_pool = sloved_pool
            self._solution_moves = []
            self._next_step = 0
            self._rand = rnd

            self._board = KTAlgorithm._init_board(self._board_size)

        def solve(self, col: int, row: int, counter: int) -> bool:
            # first move
            self._next_step += counter
            self._solution_moves.append([row, col])
            self._board[row][col] = self._next_step
            self._next_step += 1

            for i in range(pow(self._board_size, 2)):
                step_count = self._next_move(
                    {"x": self._solution_moves[i][1], "y": self._solution_moves[i][0]}
                )
                if step_count is None and self._next_step <= pow(self._board_size, 2):
                    return False

            # I did not test this, uncomment if InvalidMove exception accure. [lst97]
            # close tour (prevent invalid move on gui) may not be neccessary.
            # if self._solution_moves[-1] == self._solution_moves[0]:
            #     self._solution_moves.pop()

            self._sloved_pool.append(self._solution_moves)
            return True

        def _is_empty(self, col: int, row: int) -> bool:
            return (KTAlgorithm._validate_move(self._board, col, row)) and (
                self._board[row][col] == 0
            )

        def _get_degree(self, col: int, row: int) -> int:
            count = 0
            for i in range(len(POSSIBLE_X)):
                if self._is_empty(col + POSSIBLE_Y[i], row + POSSIBLE_X[i]):
                    count += 1
            return count

        # Warnsdorff's heuristic
        def _next_move(self, pos: dict) -> int:
            possible_move = len(POSSIBLE_X)
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
                next_x = pos["x"] + POSSIBLE_X[i]
                next_y = pos["y"] + POSSIBLE_Y[i]
                degree_count = self._get_degree(next_y, next_x)
                if self._is_empty(next_y, next_x) and degree_count < min_deg:
                    min_deg_index = i
                    min_deg = degree_count

            if min_deg_index == -1:
                return None

            # first minimum index will be pick.
            next_x = pos["x"] + POSSIBLE_X[min_deg_index]
            next_y = pos["y"] + POSSIBLE_Y[min_deg_index]

            self._solution_moves.append([next_y, next_x])
            self._board[next_x][next_y] = self._next_step
            self._next_step += 1
            return len(self._solution_moves)

    class ANN:
        # Artificial Neural Networks
        class Neuron:
            """Neuron datas"""

            def __init__(self) -> None:
                self.vertices = []
                self.neighbours = []
                self.outputs = np.array([])
                self.states = np.array([])

        def __init__(self, board_size: int, sloved_pool: list = []) -> None:
            print("Searching for solution using Artificial Neural Networks...")
            self._neuron = self.Neuron()
            self._board_size = board_size  # square board
            self._board = []

            for _ in range(self._board_size):
                temp = []
                for _ in range(self._board_size):
                    temp.append(set())
                self._board.append(temp)

            self._sloved_pool = sloved_pool
            self.allow_invalid = False  # for assessment

            """
            Finds all the possible neurons(knight moves) on the board
            and sets the neuron_vertices and neuron neighbours.
            """
            # looping through the board
            neuron_relation_num = 0
            for current_vertex_x in range(self._board_size):
                for current_vertex_y in range(self._board_size):
                    current_pos_full_index = (
                        current_vertex_x * self._board_size + current_vertex_y
                    )

                    for (target_vertex_x, target_vertex_y) in self._get_valid_move(
                        current_vertex_x, current_vertex_y
                    ):
                        target_pos_full_index = (
                            target_vertex_x * self._board_size + target_vertex_y
                        )

                        # each neuron has 2 vertices so this is to make
                        # sure that we add the neuron once.
                        if (
                            target_pos_full_index > current_pos_full_index
                        ):  # prevent duplication? lst97
                            self._board[current_vertex_x][current_vertex_y].add(
                                neuron_relation_num
                            )
                            self._board[target_vertex_x][target_vertex_y].add(
                                neuron_relation_num
                            )
                            self._neuron.vertices.append(
                                {
                                    (current_vertex_x, current_vertex_y),
                                    (target_vertex_x, target_vertex_y),
                                }
                            )
                            neuron_relation_num += 1

            # i actually is neuron_relation_num
            for i in range(len(self._neuron.vertices)):
                target_vertex, current_vertex = self._neuron.vertices[i]

                # neighbours of neuron i = neighbours of current_pos_vertex + neighbours of target_pos_vertex - i
                neighbours = self._board[current_vertex[0]][current_vertex[1]].union(
                    self._board[target_vertex[0]][target_vertex[1]]
                ) - {i}

                self._neuron.neighbours.append(neighbours)

        def solve(self, row: int, col: int, _=None) -> None:
            while True:
                iterations = 0
                self._initialize_neurons()
                is_degree_two = False

                while True:
                    _, num_of_changes = self._update_neurons()

                    if num_of_changes == 0:
                        break

                    if self._check_degree():
                        is_degree_two = True
                        break

                    # more likely a independ solution if high iterations
                    # depend solution usually accure with iterations <= 22
                    iterations += 1
                    if iterations == MAX_ITERATION:
                        break

                if is_degree_two:
                    print("Possible solution found (degree=2)...", end="")
                    solution = self._get_solution(row, col)
                    if self.allow_invalid is True:
                        self._sloved_pool.append(solution)
                    if self._check_connected_components():
                        print("Valid!")
                        self._sloved_pool.append(self._get_solution(row, col))
                        break
                    else:
                        print("Droped!")
                        is_degree_two = False

        def _initialize_neurons(self):
            """
            Initializes each neuron state to 0 and a random number
            between 0 and 1 for neuron outputs.

            """
            self._neuron.outputs = nprnd.randint(
                2, size=(len(self._neuron.vertices)), dtype=np.int16
            )
            self._neuron.states = np.zeros((len(self._neuron.vertices)), dtype=np.int16)
            pass

        def _check_degree(self):
            # gets the index of active neurons.
            active_neuron_indices = np.argwhere(self._neuron.outputs == 1).ravel()
            degree = np.zeros((self._board_size, self._board_size), dtype=np.int16)

            for i in active_neuron_indices:
                target_vertex, current_vertex = self._neuron.vertices[i]
                degree[current_vertex[0]][current_vertex[1]] += 1
                degree[target_vertex[0]][target_vertex[1]] += 1

            # if all the degrees=2 return True
            return (
                True if degree[degree == 2].size == pow(self._board_size, 2) else False
            )

        def _dfs_through_neurons(self, neuron, active_neurons):
            # removes the neuron from the active neurons list.
            active_neurons = np.setdiff1d(active_neurons, [neuron])
            # first finds the neighbours of this neuron and then finds which of them are active.
            active_neighbours = np.intersect1d(
                active_neurons, list(self._neuron.neighbours[neuron])
            )
            # if there was no active neighbours for this neuron, the hamiltonian graph has been
            # fully visited.
            if len(active_neighbours) == 0:
                # we check if all the active neurons have been visited. if not, it means that there
                # are more than 1 hamiltonian graph and it's not a knight's tour.
                return True if len(active_neurons) == 0 else False

            return self._dfs_through_neurons(active_neighbours[0], active_neurons)

        def _check_connected_components(self):
            # gets the index of active neurons.
            active_neuron_indices = np.argwhere(self._neuron.outputs == 1).ravel()
            # dfs through all active neurons starting from the first element.
            connected = self._dfs_through_neurons(
                active_neuron_indices[0], active_neuron_indices
            )
            return True if connected else False

        def _get_solution(self, col, row) -> list:
            visited = []
            current_vertex = (col, row)
            # gets the index of active neurons.
            active_neuron_indices = np.argwhere(self._neuron.outputs == 1).ravel()

            while len(active_neuron_indices) != 0:
                visited.append(current_vertex)
                # finds the index of neurons that have this vertex(current_vertex).
                vertex_neighbours = list(
                    self._board[current_vertex[0]][current_vertex[1]]
                )
                # finds the active ones.
                # active neurons that have this vertex are the edges of the solution graph that
                # share this vertex.
                vertex_neighbours = np.intersect1d(
                    vertex_neighbours, active_neuron_indices
                )
                # picks one of the neighbours(the first one) and finds the other vertex of
                # this neuron(or edge) and sets it as the current one

                try:
                    current_vertex = list(
                        self._neuron.vertices[vertex_neighbours[0]]
                        - {current_vertex}  # current_vertex = previous_vertex
                    )[0]
                except IndexError:
                    return visited if self.allow_invalid is True else None

                # removes the selected neighbour from all active neurons
                active_neuron_indices = np.setdiff1d(
                    active_neuron_indices, [vertex_neighbours[0]]
                )
            return visited

        def _update_neurons(self) -> tuple:
            """
            Updates the state and output of each neuron.

            """

            # each tile/neuron possible move = len(self._neuron.vertices)
            sum_of_neighbours = np.zeros(
                (len(self._neuron.vertices)), dtype=np.int16
            )  # m
            for i in range(len(self._neuron.vertices)):  # m
                sum_of_neighbours[i] = self._neuron.outputs[
                    list(self._neuron.neighbours[i])
                ].sum()

            ##### transition rules (model)
            # each active neuron is configured so that it reaches a “stable” state
            # if and only if it has exactly two neighboring neurons that are also active
            # so why 4, the paper shows 2 instead. [lst97]
            bias = 4 - sum_of_neighbours - self._neuron.outputs
            next_state = self._neuron.states + bias
            number_of_changes = np.count_nonzero(next_state != self._neuron.states)
            self._neuron.outputs[np.argwhere(next_state > 3).ravel()] = 1
            self._neuron.outputs[np.argwhere(next_state < 0).ravel()] = 0
            self._neuron.states = next_state
            #######################

            # counts the number of active neurons which are the neurons that their output is 1.
            number_of_active = len(self._neuron.outputs[self._neuron.outputs == 1])

            return number_of_active, number_of_changes

        def _get_valid_move(self, col: int, row: int) -> set:
            """Simluar to validate move but return valid move position instead.

            Args:
                col (int): x
                row (int): y

            Returns:
                set: set of positions
            """
            neighbours = set()
            for i in range(len(POSSIBLE_X)):
                new_x, new_y = (
                    col + POSSIBLE_X[i],
                    row + POSSIBLE_Y[i],
                )
                if 0 <= new_x < self._board_size and 0 <= new_y < self._board_size:
                    neighbours.add((new_x, new_y))
            return neighbours

    def __init__(self, main_board: Board, algo) -> None:
        """init base on what algorithm the user out.

        Args:
            main_board (Board): Board class
            algo (Any): either ANN, BT or Warnsdorff
        """
        self._paths = main_board.get_paths()
        self._algo = algo(main_board.get_size())
        if isinstance(self._algo, self.ANN):
            self._algo.allow_invalid = False  # solutions that would satisfy the network that are not knight’s tours

    def get_result(self) -> list:
        """Get paths to complete a KT problem, each value is a tile posision on screen

        Raises:
            self.NoSolutionException: No solution fonund.

        Returns:
            list: paths
        """
        path_log = []
        path_log.append(self._paths[:])
        self._algo.solve(self._paths[0][1], self._paths[0][0], 1)
        if len(self._algo._sloved_pool) != 0:
            if isinstance(self._algo, self.BT):
                self._algo._sloved_pool[0].append(
                    [self._paths[0][1], self._paths[0][0]]
                )  # change the index if multiple reuslt accure
                self._algo._sloved_pool[0] = self._algo._sloved_pool[0][
                    ::-1
                ]  # reverse order due to recursion.
        else:
            raise self.NoSolutionException()
        return self._algo._sloved_pool
