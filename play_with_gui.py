import random

import pygame

from Board import Board
from AI import minimax

BACKGROUND = (160, 160, 160, 255)
LINES = (0, 0, 0, 255)
RED = (255, 0, 0, 255)
YELLOW = (255, 255, 0, 255)

OPACITY = 80
OPACITY_RED = (255, 0, 0, OPACITY)
OPACITY_YELLOW = (255, 255, 0, OPACITY)


def play(board: Board = None, cell_width=50, ai=False, ai_depth=7, ai_starts=False, wait_between_turns=500):
    if board is None:
        board = Board((7, 6))
    
    pygame.init()
    size = (cell_width * board.size[0], cell_width * board.size[1])
    screen = pygame.display.set_mode(size)
    background = screen.convert_alpha()
    surface = screen.convert_alpha()

    pygame.display.set_caption("Connect 4" if not ai else "Connect 4: Human Vs Computer")

    background.fill(BACKGROUND)
    surface.fill((0, 0, 0, 0))
    for col in range(1, board.size[0]):
        pygame.draw.line(background, LINES, (col * cell_width, 0), (col * cell_width, size[1]))
    for row in range(1, board.size[1]):
        pygame.draw.line(background, LINES, (0, row * cell_width), (size[0], row * cell_width))

    done = False
    game_on = True
    current_color = YELLOW
    current_opacity_color = OPACITY_YELLOW

    if ai_starts and ai:
        best_game_state, best_move = minimax(board, ai_depth, maximizing_player=ai_starts)
        print(best_game_state, best_move)
        draw_piece(surface, RED, best_move, board.piles_height[best_move], cell_width,
                   board.size[1])
        board.turn(best_move)
    while not done:
        mouse_pos = pygame.mouse.get_pos()
        mouse_on_column = mouse_pos[0] // cell_width

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_column in board.available_cols and game_on:
                    draw_piece(surface, current_color, mouse_on_column, board.piles_height[mouse_on_column], cell_width,
                               board.size[1])
                    board.turn(mouse_on_column)
                    current_color = RED if current_color == YELLOW else YELLOW
                    current_opacity_color = OPACITY_RED if current_opacity_color == OPACITY_YELLOW else OPACITY_YELLOW
                    update_screen(screen, background, surface)
                    pygame.time.wait(wait_between_turns)

                    if abs(board.state_value()) == float('inf'):
                        game_on = False
                        if ai:
                            print("GAME OVER- You Won")
                            pygame.display.set_caption("Connect 4: GAME OVER- You Won")
                        else:
                            print("Game Over")
                            pygame.display.set_caption("Connect 4: GAME OVER")

                    elif ai:
                        pygame.display.set_caption("Connect 4: AI Thinking...")
                        best_game_state, best_move = minimax(board, ai_depth, maximizing_player=ai_starts)
                        pygame.display.set_caption("Connect 4")
                        if best_move is None:
                            best_move = random.choice(board.available_cols)
                            print("AI chose randomly")
                        print(best_game_state, best_move)
                        draw_piece(surface, current_color, best_move, board.piles_height[best_move],
                                   cell_width,
                                   board.size[1])

                        board.turn(best_move)
                        current_color = RED if current_color == YELLOW else YELLOW
                        current_opacity_color = OPACITY_RED if current_opacity_color == OPACITY_YELLOW else OPACITY_YELLOW
                        update_screen(screen, background, surface)
                        if abs(board.state_value()) == float('inf'):
                            game_on = False
                            pygame.display.set_caption("Connect 4: GAME OVER- AI Won")
                            print("GAME OVER- AI won")
                        pygame.time.wait(wait_between_turns)

        if game_on:
            for i in range(board.size[0]):
                if i in board.available_cols:
                    if i == mouse_on_column:
                        draw_piece(surface, current_opacity_color, mouse_on_column,
                                   board.piles_height[mouse_on_column], cell_width, board.size[1])
                    else:
                        draw_piece(surface, (0, 0, 0, 0), i, board.piles_height[i], cell_width, board.size[1])

        update_screen(screen, background, surface)


def draw_piece(surface, color, col, row, cell_width, board_height):
    row = board_height - row
    pygame.draw.circle(surface, color, (col * cell_width + cell_width // 2, row * cell_width - cell_width // 2),
                       cell_width * 2 / 5)


def update_screen(screen, background, surface):
    screen.blit(background, (0, 0))
    screen.blit(surface, (0, 0))
    pygame.display.flip()
