import copy
import random

from Board import Board


def best_move(board: Board, depth: int, alpha=-float('inf'), beta=+float('inf'), maximizing_player=True):
    """
    Calculate the best move to play using the minimax algorithm.
    This algorithm is fully deterministic but yet, because of time limits and irrational players, you can still lose a
    game using this algorithm.

    :param board: The board of th game.
    :param depth: Number of steps to look into the future. Warning: has an exponential time growth.
    :param alpha: Used to improve the average time.
    :param beta: Used to improve the average time.
    :param maximizing_player: Determines the goal of the player. It tries to get the maximal or the minimal score.
    :return: Best game-state that can be leaded to, The best move you can make.
    """
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
                        print("Unavailable column. Please choose other one.")
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