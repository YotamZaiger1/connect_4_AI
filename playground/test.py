from AI import play_against_ai
from Board import Board, Score
from play_with_gui import play


def main(*_):
    # b = Board((7, 6))  # do not increase too much
    # you_start = True
    #
    # ai_moves_to_the_future = 4  # do not increase too much!!
    #
    # # for x in [3, 0, 2, 1, 3, 0, 4, 5, 1, 0, 0, 2, 3, 3, 6, 0, 5, 0, 4, 6, 4]:
    # #
    # #     b.turn(x)
    # # # b.current_turn = True
    # # # b.printb()
    # # print(ai(b, ai_moves_to_the_future, maximizing_player=not you_start))
    # #
    # print(f"moves: {','.join([str(x) for x in play_against_ai(b, ai_moves_to_the_future, you_start)])}")
    #
    # # for x in [3,3,2,4,4,3,1,0,5,0,0,1,2,2,4,1,1]:
    # #     b.turn(x)
    # # print(b)
    # # b.printb()
    # # print(best_move(b, 7, maximizing_player=False))
    # # b.turn(3)
    # # print(b.state_value())
    # # [3, 0, 4, 0, 5, 0]
    # # [3, 0, 2, 1, 3, 0, 4, 5, 1, 0, 0, 2, 3, 3, 6, 0, 5, 0, 4]
    # # [3, 0, 2, 1, 3, 0, 4, 5, 1, 0, 0, 2, 3, 3, 6, 0, 5, 0, 4, 6, 4]
    print(play(Board((7, 6)), cell_width=100, ai=True, ai_starts=True, ai_depth=7, wait_between_turns=0))

    a = Score(5, False)
    b = Score(2, False)
    print(a <= b)


if __name__ == '__main__':
    main()
