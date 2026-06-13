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

START_POSITIONS = [
    (0, 0), (0, 3), (0, 7),
    (7, 0), (7, 3), (7, 7)
]

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

whites = ("R", "N", "B", "Q", "K", "P")
blacks = ("r", "n", "b", "q", "k", "p")

start_board = "RNBKQBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbkqbnr"
start_board = "R11K111R/PPPPPPPP/8/8/8/8/pppppppp/r11k111r"

# start_board = "111P1111/1P11P111/11P11111/1rp1BN11/P1111111/11K11111/11Q111P1/1p111111"

pygame.init()

screen = pygame.display.set_mode((BOARD_SIZE + PADDING * 2, BOARD_SIZE + PADDING * 2))

clock = pygame.time.Clock()

pygame.display.set_caption("CHESS")

def generate_board(schema):
    board_schema = schema.split("/")

    board = []

    for item in board_schema:
        squares = []

        for char in item:
            if char.isdigit():
                squares.extend([""] * int(char))
            else:
                squares.append(char)

        board.append(squares)
    
    return board

def render_board(data, screen):
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

    if selection: draw_selection(*selection)

    draw_suggestion(suggestions)

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

def has_figure(color, row, col):
    if color == "white":
        return board[row][col].isupper()
    elif color == "black":
        return board[row][col].islower()
    
def draw_selection(row, col):
    if row == None or col == None:
        return
    
    x = col * SQUARE_SIZE + PADDING
    y = row * SQUARE_SIZE + PADDING
    
    pygame.draw.rect(screen, (100, 150, 255), (x, y, SQUARE_SIZE, SQUARE_SIZE), 4)

def get_figures(color):
    colored = whites if color == "white" else blacks
    figures = []

    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] in colored:
                figures.append((row, col))

    return figures

def can_go(figure, row, col):
    if (col > 7 or col < 0) or (row > 7 or row < 0):
        return (False, False)
    
    return (
        (figure in whites and board[row][col] not in whites) or (figure in blacks and board[row][col] not in blacks), 
        board[row][col] == ""
    )

def is_safe(row, col, enemies):
    safe = True

    figure = board[row][col]
    board[row][col] = "P"

    for enemy in enemies:
        if (row, col) in get_moves(*enemy, False):
            safe = False
            break

    board[row][col] = figure

    return safe

def get_line_moves(figure, row, col, r_shift, c_shift):
    moves = []

    i = row + r_shift
    j = col + c_shift

    while 0 <= i < len(board) and 0 <= j < len(board):
        here, further = can_go(figure, i, j)
        if not here: break

        moves.append((i, j))

        if not further or figure in "KkNnPp": break

        i += r_shift
        j += c_shift
    
    return moves

def get_pawn_moves(figure, row, col):
    r_shift = 1 if figure in whites else - 1

    moves = []

    here, further = can_go(figure, row + r_shift, col)
    if here and further: moves.append((row + r_shift, col))

    if moves and (row == 1 or row == 6): 
        here, further = can_go(figure, row + r_shift * 2, col)
        if here and further: moves.append((row + r_shift * 2, col))

    here, further = can_go(figure, row + r_shift, col - 1)
    if (here and not further): moves.append((row + r_shift, col - 1))

    here, further = can_go(figure, row + r_shift, col + 1)
    if (here and not further): moves.append((row + r_shift, col + 1))

    return moves

def get_rook_moves(figure, row, col):
    return [
        *get_line_moves(figure, row, col, 0, 1), 
        *get_line_moves(figure, row, col, 1, 0), 
        *get_line_moves(figure, row, col, 0, -1), 
        *get_line_moves(figure, row, col, -1, 0),
    ]
    
def get_knight_moves(figure, row, col):
    return [
        *get_line_moves(figure, row, col, 1, 2),
        *get_line_moves(figure, row, col, 2, 1),
        *get_line_moves(figure, row, col, 2, -1),
        *get_line_moves(figure, row, col, 1, -2),
        *get_line_moves(figure, row, col, -1, -2),
        *get_line_moves(figure, row, col, -2, -1),
        *get_line_moves(figure, row, col, -2, 1),
        *get_line_moves(figure, row, col, -1, 2),
    ]

def get_bishop_moves(figure, row, col):
    return [
        *get_line_moves(figure, row, col, 1, 1), 
        *get_line_moves(figure, row, col, 1, -1), 
        *get_line_moves(figure, row, col, -1, 1), 
        *get_line_moves(figure, row, col, -1, -1), 
    ]

def get_royal_moves(figure, row, col, real=True):
    moves = [
        *get_bishop_moves(figure, row, col),
        *get_rook_moves(figure, row, col)
    ]

    if figure in "Kk" and real: 
        color = "black" if figure in whites else "white"
        enemies = get_figures(color)
        moves = list(filter(lambda move: is_safe(*move, enemies), moves))

    return moves

def get_king_moves(figure, row, col, real=True):
    moves = get_royal_moves(figure, row, col, real)

    if (row, col) in START_POSITIONS:
        color = "black" if figure in whites else "white"
        enemies = get_figures(color)

        if (row, 0) in START_POSITIONS and (row, 2) in moves and not board[row][1] and is_safe(row, 1, enemies):
            moves.append((row, 1))

        if (row, 7) in START_POSITIONS and (row, 4) in moves and not (board[row][6] or board[row][5]) and is_safe(row, 5, enemies):
            moves.append((row, 5))

    return moves

def get_moves(row, col, real=True):
    figure = board[row][col]
    
    if not figure:
        return []

    if figure in "Pp":
        return get_pawn_moves(figure, row, col)
    
    if figure in "Rr":
        return get_rook_moves(figure, row, col)
    
    if figure in "Nn":
        return get_knight_moves(figure, row, col)
    
    if figure in "Bb":
        return get_bishop_moves(figure, row, col)

    if figure in "Qq":
        return get_royal_moves(figure, row, col)
    
    if figure in "Kk":
        return get_king_moves(figure, row, col, real)
    
    return []
        
def draw_suggestion(moves):
    for row, col in moves:
        x = col * SQUARE_SIZE + PADDING
        y = row * SQUARE_SIZE + PADDING

        square_rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
        
        pygame.draw.circle(screen, (175, 205, 100), square_rect.center, 10)

def make_move(row, col):
    global selection, current_player, suggestions

    r, c = selection

    board[row][col] = board[r][c]
    board[r][c] = ""

    current_player = "black" if current_player == "white" else "white"

    selection = None
    suggestions = []

board = generate_board(start_board)

selection = None
suggestions = []

current_player = "white"

while True:
    clock.tick(60)

    screen.fill(BG_COLOR)
    render_board(board, screen)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            col = (mouse_x - PADDING) // SQUARE_SIZE
            row = (mouse_y - PADDING) // SQUARE_SIZE

            if 0 <= row < ROWS and 0 <= col < COLS:
                target = (row, col)

                if selection and target in suggestions:
                    make_move(*target)
                if has_figure(current_player, row, col):
                    selection = (row, col)
                    suggestions = get_moves(row, col)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                current_player = "black" if current_player == "white" else "white"

    pygame.display.update()