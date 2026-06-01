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

board_rect = pygame.Rect(PADDING, PADDING, BOARD_SIZE, BOARD_SIZE)
board_surface = screen.subsurface(board_rect)

pygame.display.set_caption("CHESS")

def generate_board(rows, cols):
    board = []

    for row in range(rows):
        squares = []

        for col in range(cols):
            if (row + col) % 2 == 0:
                squares.append("w")
            else:
                squares.append("b")

        board.append(squares)

    return board

def render_board(data):
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            color = LIGHT_COLOR if item == "w" else DARK_COLOR

            x = j * SQUARE_SIZE
            y = i * SQUARE_SIZE 

            pygame.draw.rect(board_surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

board = generate_board(ROWS, COLS)

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BG_COLOR)

    render_board(board)

    pygame.display.update()