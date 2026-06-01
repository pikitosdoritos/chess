import pygame
import json

SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
PADDING = 50
COLS = 8 
ROWS = 8

running = True

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
    pass

def format_output(data):
    json_text = json.dumps(data)
    
    return json_text.replace("],", "],\n")

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.flip()

print(format_output(generate_board(ROWS, COLS)))