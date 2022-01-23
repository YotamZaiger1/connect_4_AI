# connect_4_AI
An algorithm to win the famous "connect 4" game.

Using the `minimax` algorithm, choose the best move to play.<br />
The algorithm searches for the best move it can make by considering the possible outcomes in the future of the game.
The algorithm looks into the future in a certain depth, and in that scope of view it plays the game perfectly.<br />
If the algorithm finds a way that theoreticly it would lose (if the opponent will play perfectly), it will delay the lost or avoid it as good as posible.


## Usage/Examples

- To play against the AI with simple ASCII preview:
    ```python
    from AI import play_against_ai
    from Board import Board

    board = Board(size=(7, 6))
    play_against_ai(board, depth=5, you_start=True)
    ```
    
- To play against the AI or a friend with GUI preview:
    ```python
    from play_with_gui import play
    from Board import Board

    board = Board(size=(7, 6))
    play(board, ai=True, ai_starts=False, ai_depth=5, cell_width=100, wait_between_turns=0)
    ```

**Notice**: Do not increase the AI `depth` parameter or the size of the board too much. It will take long time for the algorithm to finish running.


## Requirements

- python3 and above.
- for the GUI version- pygame.
    To install use:
    ```bash
    pip install pygame
    ```
    in your terminal.


## Screenshots
<img width="700" src="https://github.com/YotamZaiger1/connect_4_AI/blob/master/Screenshot.png">
