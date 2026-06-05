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

symbols = {
        "P": "♙",
        "R": "♖",
        "N": "♘",
        "B": "♗",
        "Q": "♕",
        "K": "♔",

        "p": "♟",
        "r": "♜",
        "n": "♞",
        "b": "♝",
        "q": "♛",
        "k": "♚",
    }

start_board = "RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr"

pygame.init()

screen = pygame.display.set_mode((BOARD_SIZE + PADDING * 2, BOARD_SIZE + PADDING * 2))

clock = pygame.time.Clock()

pygame.display.set_caption("CHESS")

def generate_clear_board():
    board = []

    for row in range(ROWS):
        squares = []

        for col in range(COLS):
            squares.append(" ")

        board.append(squares)

    return board

def generate_board(data):
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if i == 0:
                row[j] = start_board[j]
            elif i == 1:
                row[j] = "P"
            elif i == 6:
                row[j] = "p"
            elif i == 7:
                row[j] = start_board[(-1) + (-j)]
            
    return data

def render_board(data, screen, selection):
    font = pygame.font.SysFont("segoeuisymbol", 70)
    board_rect = pygame.Rect(PADDING, PADDING, BOARD_SIZE, BOARD_SIZE)

    board_surface = screen.subsurface(board_rect)

    for i, row in enumerate(data):
        for j, item in enumerate(row):
            color = LIGHT_COLOR if (i + j) % 2 == 0 else DARK_COLOR

            x = j * SQUARE_SIZE
            y = i * SQUARE_SIZE 

            square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            
            if item != " ":
                figure = symbols.get(item)
                figure_text = font.render(figure, True, (0, 0, 0))
                figure_rect = figure_text.get_rect(center=square_rect.center)

            pygame.draw.rect(board_surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            board_surface.blit(figure_text, figure_rect)

    render_labels(screen)
    draw_selection(*selection)

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

def draw_selection(row, col):
    if row == None or col == None:
        return
    
    x = col * SQUARE_SIZE + PADDING
    y = row * SQUARE_SIZE + PADDING
    
    pygame.draw.rect(screen, (100, 150, 255), (x, y, SQUARE_SIZE, SQUARE_SIZE), 4)

clear_board = generate_clear_board()
board = generate_board(clear_board)

selection = [None, None]

while True:
    clock.tick(60)

    screen.fill(BG_COLOR)
    render_board(board, screen, selection)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            col = (mouse_x - PADDING) // SQUARE_SIZE
            row = (mouse_y - PADDING) // SQUARE_SIZE

            if 0 <= row < ROWS and 0 <= col < COLS:
                selection = [row, col]

    pygame.display.update()