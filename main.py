import pygame
import json
import sys

SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
PADDING = 50
COLS = 8 
ROWS = 8
LIGHT_COLOR = (240, 217, 181)
DARK_COLOR = (181, 136, 99)

pygame.init()

screen = pygame.display.set_mode((BOARD_SIZE + PADDING * 2, BOARD_SIZE + PADDING * 2))
clock = pygame.time.Clock()

def generate_board(rows, cols):
    board = []

    for row in range(rows):
        squares = []
        for col in range(cols):
            if col % 2:
                squares.append("w")
            else:
                squares.append("b")

        if row % 2:
            board.append(squares)
        else:
            change_elem = squares.pop(0)
            squares.append(change_elem)
            board.append(squares)

    return board

def render_board(data):
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item == "w":
                color = LIGHT_COLOR
            elif item == "b":
                color = DARK_COLOR

            x = j * SQUARE_SIZE
            y = i * SQUARE_SIZE

            pygame.draw.rect(screen, color, (x + PADDING, y + PADDING, SQUARE_SIZE, SQUARE_SIZE))

def format_output(data):
    json_text = json.dumps(data)
    
    return json_text.replace("],", "],\n")

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event == pygame.QUIT:
            pygame.quit()
            sys.exit()

    board = generate_board(ROWS, COLS)

    render_board(board)

    pygame.display.update()

print(format_output(generate_board(ROWS, COLS)))