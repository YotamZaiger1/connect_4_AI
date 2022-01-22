ALL_DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (1, 0)]
LINE_LENGTH_VALUE = {0: 0, 1: 0, 2: 3, 3: 10}  # maybe change a bit


class Score:
    """
    A class to extend the score values of a board state (class Board).

    Instances of this class have two options:
        - finite scores
        - infinite scores
    When two Scores instances are being compared, the infinite value being checked first and then the finite part.
    """

    def __init__(self, power=0, is_infinite=False):
        self.value = (is_infinite, power)
        if power == 0:
            is_infinite = False
        self.is_infinite = is_infinite
        self.power = power

    def __le__(self, other):
        assert isinstance(other, Score)

        if self.is_infinite and not other.is_infinite:
            return self.power < 0
        if other.is_infinite and not self.is_infinite:
            return other.power > 0

        # both finite or both infinite
        return self.power <= other.power

    def __eq__(self, other):
        return isinstance(other, Score) and self.power == other.power and self.is_infinite == other.is_infinite

    def __ge__(self, other):
        return (not self <= other) or (self == other)

    def __lt__(self, other):
        return self <= other and self != other

    def __gt__(self, other):
        return not self <= other

    def __repr__(self):
        if self.value[0]:
            return f'Inf({self.value[1]})'
        return str(self.value[1])


class Board:
    def __init__(self, size: tuple[int, int]):
        self.board = [[None for _ in range(size[1])] for _ in range(size[0])]
        self.available_cols = {i for i in range(size[0])}
        self.piles_height = [0] * size[0]

        self.turns_left = size[0] * size[1]  # number of empty cells remained
        self.size = size

        self.current_turn = False

    def __getitem__(self, item: tuple[int, int]):
        return self.board[item[0]][item[1]]

    def __setitem__(self, key: tuple[int, int], value):
        self.board[key[0]][key[1]] = value

    def turn(self, col: int):
        assert col in self.available_cols
        self[col, self.piles_height[col]] = self.current_turn

        self.piles_height[col] += 1

        if self.piles_height[col] == self.size[1]:  # column full
            self.available_cols.remove(col)

        self.current_turn = not self.current_turn
        self.turns_left -= 1

    def undo_tern(self, col: int):
        assert self[col, self.piles_height[col] - 1] is not None

        self.piles_height[col] -= 1
        self.available_cols.add(col)
        self[col, self.piles_height[col]] = None
        self.current_turn = not self.current_turn
        self.turns_left += 1

    def __repr__(self):
        return f"<Board {self.size}; Turn: {int(self.current_turn)}>"

    def printb(self, **kwargs):
        """Print the current game state with ASCII characters."""
        # "■□"
        print("_" * (self.size[0] + 2), **kwargs)
        for row in range(self.size[1]):
            row = self.size[1] - row - 1
            s = "|"
            for col in range(self.size[0]):
                if self.piles_height[col] > row:
                    if self[col, row]:
                        s += "■"
                    else:
                        s += "□"
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
        Checks how many of the same pieces are in the given line- without any pieces of the second player.
        :param origin: The starting position of the line.
        :param direction: The direction the line goes in. Vector of the x,y change.
        :return: The number of same pieces in the given line. If there are pieces of the second player returns 0.
        """
        assert self[origin] is not None
        player = self[origin]
        pos: list[int] = list(origin)
        length = 1

        for _ in range(3):  # we look for lines of 4, and we already have started with the origin point.
            pos[0] += direction[0]
            pos[1] += direction[1]

            if 0 <= pos[0] < self.size[0] and 0 <= pos[1] < self.size[1]:
                value = self[tuple(pos)]
                if value is player:
                    length += 1
                elif value is (not player):
                    return 0
                # o.w. value is None, so we add 0.
            else:
                return 0

        return length

    def state_value(self) -> Score:
        """
        The 'value' of the current game state.
        As the value gets bigger the state is better for the first player.
        In a case that the game is over:
            - If the first player has won, he gets higher score as there are more turns left.
            - If the first player has lost, he gets higher score as there are fewer turns left.

        :return
        A `Score` object. If the game is over the score will be infinite and the power will be the number-of-turns-left-
        to-the-game + 1. Otherwise, the score will be finite and the power will be the 'value' of the game-state for the
        first player.
        """
        f_value = 0  # the first player progress
        t_value = 0  # the second players progress
        for col in range(self.size[0]):
            for row in range(self.piles_height[col]):
                player = self[col, row]

                for direction in ALL_DIRECTIONS:
                    line_length = self.get_line_length((col, row), direction)
                    if line_length == 4:  # some player has won the game
                        if player:  # it's the second player turn
                            return Score(-(self.turns_left + 1), is_infinite=True)
                        return Score(self.turns_left + 1, is_infinite=True)

                    value = LINE_LENGTH_VALUE[line_length]
                    if player:
                        t_value += value
                    else:
                        f_value += value

        return Score(f_value - t_value, is_infinite=False)
