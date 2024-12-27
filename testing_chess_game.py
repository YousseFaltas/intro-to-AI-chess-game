import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600  # Board dimensions
SQUARE_SIZE = WIDTH // 8  # Size of each square
WHITE = (255, 255, 255)   # White square color
GREEN = (47, 114, 87)         # Green square color

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")


# Load Piece Images
PIECE_IMAGES = {}
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',  # White pieces
              'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']  # Black pieces
    for piece in pieces:
        PIECE_IMAGES[piece] = pygame.transform.scale(
            pygame.image.load(f"images/{piece}.png"), 
            (SQUARE_SIZE, SQUARE_SIZE)
        )

# Draw Chessboard
def draw_board():
    colors = [WHITE, GREEN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]  # Alternate colors
            pygame.draw.rect(screen, color, 
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Initial Board Setup (8x8 Matrix)
# Uppercase = White, Lowercase = Black, "." = Empty
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
]

# Draw Pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                screen.blit(PIECE_IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def rules ( row , col , new_row , new_col, piece):
    if 'w' in piece and 'w' in board[new_row][new_col]:
            return False
    elif 'b' in piece and 'b' in board[new_row][new_col]:
            return False
    elif piece == 'bP':
        if 'w' in board[new_row][new_col]:
            if new_row == (row+1) and (new_col == (col+1) or new_col == (col-1)):
                return True
        elif row == 1: 
            if new_col == col and (new_row == (row+1) or new_row == (row+2)):  
               return True
        else:
            if new_col == col and new_row == (row+1):
                return True
    elif piece == 'wP':
        if 'b' in board[new_row][new_col]:
            if new_row == (row-1) and (new_col == (col+1) or new_col == (col-1)):
                return True
        elif row == 6: 
            if new_col == col and (new_row == (row-1) or new_row == (row-2)):  
               return True
        else:
            if new_col == col and new_row == (row-1):
                return True
    elif 'R' in piece:
        if new_row == row:
            smaller = min(new_col,col)
            bigger = max(new_col, col)
            for  i in range(smaller+1 , bigger):
                if board[new_row][i] != '.':
                    return False
                else:
                    continue   
            return True
        elif new_col==col:
            smaller = min(new_row,row)
            bigger = max(new_row, row)
            for  i in range(smaller+1, bigger):
                if board[i][new_col] != '.':
                    return False
                else:
                    continue                        
            return True
    elif 'N' in piece:
        if new_row == (row+2) or new_row == (row-2):
            if new_col== (col+1) or new_col== (col-1):
                return True
        elif new_col == (col+2) or new_col == (col-2):
            if new_row == (row+1) or new_row == (row-1):
                return True
    elif 'B' in piece:
        smal_col = min(new_col,col)
        big_col = max(new_col, col)
        smal_row = min(new_row, row)
        big_row = max(new_row, row)
        if (big_col-smal_col) == (big_row - smal_row):
            i = smal_row+1
            j = smal_col+1
            while i<big_row and j<big_col:
                if board[i][j]!='.':
                    return False
                else:
                    i+=1
                    j+=1
            return True
    elif 'Q' in piece:
        smal_col = min(new_col,col)
        big_col = max(new_col, col)
        smal_row = min(new_row, row)
        big_row = max(new_row, row)
        if (big_col-smal_col) == (big_row - smal_row):
            for i in range(smal_row+1 , big_row):
                for j in range(smal_col+1 , big_col):
                    if board[i][j]!='.':
                        return False
                    else:
                        continue
            return True
        elif new_row == row:
            for  i in range(smal_col+1 , big_col):
                if board[new_row][i] != '.':
                    return False
                else:
                    continue   
            return True
        elif new_col==col:
            for  i in range(smal_row+1, big_row):
                if board[i][new_col] != '.':
                    return False
                else:
                    continue                        
            return True
    elif 'K' in piece:
        if new_row in  range(row-1,row+1) and new_col in range(col-1,col+1):
            return True
        
    return False


# Main Game Loop
def main():
    piece = None
    dragging_piece= None
    dragging_piece_pos = None
    dragging_piece_offset = None 
    load_images()  # Load piece images
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                if board[row][col] != '.':  # If there's a piece on the square
                    piece = board[row][col]
                    dragging_piece = board[row][col]
                    dragging_piece_pos = (row, col)
                    dragging_piece_offset = (mouse_x % SQUARE_SIZE, mouse_y % SQUARE_SIZE)
                    board[row][col] = '.'  # Remove piece from the board temporarily
                    
            # Mouse Motion - Dragging the Piece
            elif event.type == pygame.MOUSEMOTION:
                if dragging_piece :
                    mouse_x, mouse_y = event.pos
            
            # Mouse Button Up - Drop the Piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_piece:
                    mouse_x, mouse_y = event.pos
                    col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                    old_row, old_col = dragging_piece_pos
                    # Drop the piece on the new square
                    if rules(old_row , old_col , row , col , dragging_piece):
                        board[row][col] = dragging_piece
                        dragging_piece = None
                    else:
                        board[old_row][old_col] = dragging_piece
                        dragging_piece = None

        # Draw Board and Pieces
        draw_board()
        draw_pieces()
        
        # Draw Dragging Piece
        if dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(PIECE_IMAGES[dragging_piece], 
                        (mouse_x - dragging_piece_offset[0], mouse_y - dragging_piece_offset[1]))

        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()