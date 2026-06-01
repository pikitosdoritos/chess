import pygame
import sys

SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
PADDING = 50

COLS = 8 
ROWS = 8

LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)
BG_COLOR = (30, 30, 30)

pygame.init()

screen = pygame.display.set_mode((BOARD_SIZE + PADDING * 2, BOARD_SIZE + PADDING * 2))

clock = pygame.time.Clock()

pygame.display.set_caption("CHESS")

def generate_board():
    board = []

    for row in range(ROWS):
        squares = []

        for col in range(COLS):
            if (row + col) % 2 == 0:
                squares.append("w")
            else:
                squares.append("b")

        board.append(squares)

    return board

def render_board(data, screen):
    board_rect = pygame.Rect(PADDING, PADDING, BOARD_SIZE, BOARD_SIZE)
    board_surface = screen.subsurface(board_rect)

    for i, row in enumerate(data):
        for j, item in enumerate(row):
            color = LIGHT_COLOR if item == "w" else DARK_COLOR

            x = j * SQUARE_SIZE
            y = i * SQUARE_SIZE 

            pygame.draw.rect(board_surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    render_labels(screen)

def render_labels(surface):
    font = pygame.font.Font(None, 50)

    h_surface = pygame.Surface((BOARD_SIZE, PADDING), pygame.SRCALPHA)
    v_surface = pygame.Surface((PADDING, BOARD_SIZE), pygame.SRCALPHA)

    for i in range(ROWS):
        letter = chr(97 + i)

        text_surface = font.render(letter, True, LIGHT_COLOR)
        rect = pygame.Rect(i * SQUARE_SIZE, 0, SQUARE_SIZE, PADDING)

        text_rect = text_surface.get_rect(center=rect.center)

        h_surface.blit(text_surface, text_rect)
    
    for j in range(COLS):
        number_surface = font.render(str(j+1), True, LIGHT_COLOR)

        rect = pygame.Rect(0, j * SQUARE_SIZE, PADDING, SQUARE_SIZE)

        number_rect = number_surface.get_rect(center=rect.center)

        v_surface.blit(number_surface, number_rect)

    surface.blit(h_surface, (PADDING, 0))
    surface.blit(h_surface, (PADDING, PADDING + BOARD_SIZE))
    surface.blit(v_surface, (0, PADDING))
    surface.blit(v_surface, (PADDING + BOARD_SIZE, PADDING))

board = generate_board()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    render_board(board, screen)

    pygame.display.update()