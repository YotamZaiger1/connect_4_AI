import copy
import random

ALL_DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (1, 0)]
LINE_LENGTH_VALUE = {0: 0, 1: 0, 2: 3, 3: 10}


class Board:
    __slots__ = ["board", "available_cols", "size", "current_turn"]

    def __init__(self, size: tuple[int, int]):
        self.board = [list() for _ in range(size[0])]
        self.available_cols = {i for i in range(size[0])}
        self.size = size

        self.current_turn = False

    def __getitem__(self, item: tuple[int, int]):
        assert item[0] < self.size[0] and item[1] < self.size[1]
        if item[1] >= len(self.board[item[0]]):
            return None
        return self.board[item[0]][item[1]]

    def turn(self, col: int):
        assert col in self.available_cols
        self.board[col].append(self.current_turn)

        if len(self.board[col]) == self.size[1]:  # column full
            self.available_cols.remove(col)

        self.current_turn = not self.current_turn

    def __repr__(self):
        return f"<Board {self.size}; Turn: {int(self.current_turn)}>"

    def printb(self, **kwargs):
        """Print the game state in ASCII."""
        # "■□"
        print("_" * (self.size[0] + 2), **kwargs)
        for row in range(self.size[1]):
            row = self.size[1] - row - 1
            s = "|"
            for col in range(self.size[0]):
                if len(self.board[col]) > row:
                    s += "■" if self[col, row] else "□"
                else:
                    s += " "
            s += "|"
            print(s, **kwargs)

        print("_" * (self.size[0] + 2), **kwargs)
        if self.size[0] <= 10:
            print("|" + ''.join([str(x) for x in range(self.size[0])]) + "|", **kwargs)
            print("‾" * (self.size[0] + 2), **kwargs)

    ####################################################################

    def get_line_length(self, origin: tuple[int, int], direction: tuple[int, int]):
        """
        Checks how many of the same pieces are in the given line- without any of the second player.
        :param origin: The starting position of the line.
        :param direction: The direction the line goes in. Vector of the x,y change.
        :return: The number of same pieces in the given line. If there are pieces of the second player returns 0.
        """
        assert self[origin] is not None
        player: bool = self[origin]
        pos: list[int] = list(origin)
        length = 1

        for _ in range(3):  # we look for lines of 4, and we already have started with the origin point.
            pos[0] += direction[0]
            pos[1] += direction[1]

            if 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]:
                value = self[tuple(pos)]
                if value is player:
                    length += 1
                elif value is not player:
                    return 0
                # o.w. value is None, so we add 0.
            else:
                return 0

        return length

    def state_value(self):
        """
        The `value` of the current game state.
        As the value gets bigger the state is better for the first player.
        """
        f_value = 0  # the first player progress
        t_value = 0  # the second players progress
        for col in range(self.size[0]):
            for row in range(len(self.board[col])):
                player = self[col, row]

                for direction in ALL_DIRECTIONS:
                    line_length = self.get_line_length((col, row), direction)
                    if line_length == 4:  # some player has won the game
                        return -float('inf') if player else float('inf')

                    value = LINE_LENGTH_VALUE[line_length]
                    if player:
                        t_value += value
                    else:
                        f_value += value

        return f_value - t_value


def best_move(board: Board, depth: int, alpha=-float('inf'), beta=+float('inf'), maximizing_player=True):
    state_value = board.state_value()
    if depth == 0 or abs(state_value) == float('inf'):  # 0 depth or game over
        return state_value, None

    move = None
    if maximizing_player:
        max_eval = -float('inf')
        for col in board.available_cols:
            new_board = copy.deepcopy(board)
            new_board.turn(col)
            evaluation = best_move(new_board, depth - 1, alpha, beta, maximizing_player=False)[0]
            if evaluation > max_eval:
                max_eval = evaluation
                move = col
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break

        return max_eval, move

    else:
        min_eval = +float('inf')
        for col in board.available_cols:
            new_board = copy.deepcopy(board)
            new_board.turn(col)
            evaluation = best_move(new_board, depth - 1, alpha, beta, maximizing_player=True)[0]
            if evaluation < min_eval:
                min_eval = evaluation
                move = col
            beta = min(beta, evaluation)
            if beta <= alpha:
                break

        return min_eval, move


def play_against_ai(board, depth, you_start=True):
    history = []
    while True:
        board.printb()
        value = board.state_value()
        if abs(value) == float('inf'):
            if board.current_turn == you_start:
                print("Congratulations! You won!")
            else:
                print("AI won. :(")
            break

        if board.current_turn != you_start:
            while True:
                col = input(">>>")
                if col == 'c':
                    break
                try:
                    col = int(col)
                    if col not in board.available_cols:
                        print("Unavailable column. Please chose other one.")
                        continue
                    break
                except ValueError:
                    pass

        else:
            col = best_move(board, depth, maximizing_player=not you_start)[1]
            if col is None:
                col = random.choice(list(board.available_cols))
                print("(Random)")
            print(f"AI moved in column number {col}.")

        if col == 'c':
            break
        print(board.state_value())
        board.turn(col)
        history.append(col)
        print(board.state_value())

    return history


if __name__ == '__main__':
    b = Board((7, 6))  # do not increase too much
    you_start = True
    ai_moves_to_the_future = 7  # do not increase!!

    print(f"moves: {','.join([str(x) for x in play_against_ai(b, ai_moves_to_the_future, you_start)])}")
    # b = Board((7, 6))
    # for x in [3, 0, 2, 1, 3, 0, 4, 5, 1, 0, 0, 2, 3, 3, 6, 0, 5, 0, 4]:
    #     b.turn(x)
    # print(best_move(b, 6, maximizing_player=False))
