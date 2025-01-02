import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600  # Board dimensions
SQUARE_SIZE = 600 // 8  # Size of each square
WHITE = (255, 255, 255)  # White square color
GREEN = (47, 114, 87)  # Green square color
SIDE_COLOR = (200, 200, 200)  # Light gray color for the side area
current_turn = 'white'  # 'white' or 'black'

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Piece Values
PIECE_VALUES = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100
}

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

# Lists to store captured pieces
captured_white = []
captured_black = []

# Draw Pieces
def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                screen.blit(PIECE_IMAGES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Draw Side Area Background
def draw_side_area():
    pygame.draw.rect(screen, SIDE_COLOR, (600, 0, 400, 600))

# Draw Captured Pieces
def draw_captured_pieces():
    draw_side_area()
    white_x, white_y = 610, 20  # Position for captured white pieces
    black_x, black_y = 610, HEIGHT // 2 + 20  # Position for captured black pieces
    for i, piece in enumerate(captured_white):
        screen.blit(PIECE_IMAGES[piece], (white_x + (i % 4) * (SQUARE_SIZE // 2), white_y + (i // 4) * (SQUARE_SIZE // 2)))
    for i, piece in enumerate(captured_black):
        screen.blit(PIECE_IMAGES[piece], (black_x + (i % 4) * (SQUARE_SIZE // 2), black_y + (i // 4) * (SQUARE_SIZE // 2)))

# Rules for Piece Movement
def rules(row, col, new_row, new_col, piece):
    global captured_white, captured_black

    # Prevent moving to the same square
    if row == new_row and col == new_col:
        return False

    # Prevent capturing your own pieces
    target_piece = board[new_row][new_col]
    if ('w' in piece and 'w' in target_piece) or ('b' in piece and 'b' in target_piece):
        return False

    # Calculate row and column differences
    row_diff = new_row - row  # Positive if moving down, negative if moving up
    col_diff = abs(new_col - col)

    # Pawn movement
    if 'P' in piece:
        direction = -1 if 'w' in piece else 1  # White pawns move up (negative row), black pawns move down (positive row)
        # Check for valid pawn move
        if col == new_col:  # Moving straight
            if row_diff == direction and target_piece == '.':  # Normal move
                return True
            elif row_diff == 2 * direction and (row == 6 and 'w' in piece or row == 1 and 'b' in piece) and target_piece == '.' and board[row + direction][col] == '.':  # Double move on first move
                return True
        elif col_diff == 1 and row_diff == direction:  # Capturing diagonally
            if target_piece != '.':  # Ensure there's a piece to capture
                if 'w' in target_piece and target_piece not in captured_white:
                    captured_white.append(target_piece)
                    print(f"Captured White Piece: {target_piece}")  # Debugging
                elif 'b' in target_piece and target_piece not in captured_black:
                    captured_black.append(target_piece)
                    print(f"Captured Black Piece: {target_piece}")  # Debugging
                return True
        return False

    # Rook movement
    elif 'R' in piece:
        if row == new_row:  # Moving horizontally
            step = 1 if new_col > col else -1
            for c in range(col + step, new_col, step):
                if board[row][c] != '.':
                    return False
            return True
        elif col == new_col:  # Moving vertically
            step = 1 if new_row > row else -1
            for r in range(row + step, new_row, step):
                if board[r][col] != '.':
                    return False
            return True
        return False

    # Knight movement
    elif 'N' in piece:
        if (abs(row_diff) == 2 and abs(col_diff) == 1) or (abs(row_diff) == 1 and abs(col_diff) == 2):
            return True
        return False

    # Bishop movement
    elif 'B' in piece:
        if abs(row_diff) == abs(col_diff):  # Moving diagonally
            row_step = 1 if new_row > row else -1
            col_step = 1 if new_col > col else -1
            r, c = row + row_step, col + col_step
            while r != new_row and c != new_col:
                if board[r][c] != '.':
                    return False
                r += row_step
                c += col_step
            return True
        return False

    # Queen movement (combination of rook and bishop)
    elif 'Q' in piece:
        if row == new_row or col == new_col:  # Rook-like movement
            if row == new_row:
                step = 1 if new_col > col else -1
                for c in range(col + step, new_col, step):
                    if board[row][c] != '.':
                        return False
            else:
                step = 1 if new_row > row else -1
                for r in range(row + step, new_row, step):
                    if board[r][col] != '.':
                        return False
            return True
        elif abs(row_diff) == abs(col_diff):  # Bishop-like movement
            row_step = 1 if new_row > row else -1
            col_step = 1 if new_col > col else -1
            r, c = row + row_step, col + col_step
            while r != new_row and c != new_col:
                if board[r][c] != '.':
                    return False
                r += row_step
                c += col_step
            return True
        return False

    # King movement
    elif 'K' in piece:
        if abs(row_diff) <= 1 and abs(col_diff) <= 1:
            return True
        return False

    return False  # Default case: invalid move

# Evaluate a Move Based on Heuristics
def evaluate_move(board, move, color):
    score = 0
    for row in range(8):
        for col in range(8):
            piece = move[row][col]
            if piece != '.':
                # Add piece value to the score
                score += PIECE_VALUES[piece[1]] * (1 if piece[0] == color else -1)
    return score

# Knowledge-Based Decision Maker
def make_knowledge_based_move(color):
    best_move = None
    best_score = -math.inf  # Use math.inf for initializing best_score
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.' and piece[0] == color:
                for new_row in range(8):
                    for new_col in range(8):
                        if rules(row, col, new_row, new_col, piece):
                            # Simulate the move
                            new_board = [row[:] for row in board]
                            new_board[new_row][new_col] = piece
                            new_board[row][col] = '.'
                            # Evaluate the move
                            score = evaluate_move(new_board, new_board, color)
                            if score > best_score:
                                best_score = score
                                best_move = new_board
    if best_move:
        for row in range(8):
            for col in range(8):
                board[row][col] = best_move[row][col]

# Main Game Loop
def main():
    global current_turn
    piece = None
    dragging_piece = None
    dragging_piece_pos = None
    dragging_piece_offset = None
    load_images()  # Load piece images
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_turn == 'white':  # Only allow white pieces to move
                    mouse_x, mouse_y = event.pos
                    col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                    if board[row][col] != '.' and board[row][col][0] == 'w':
                        piece = board[row][col]
                        dragging_piece = board[row][col]
                        dragging_piece_pos = (row, col)
                        dragging_piece_offset = (mouse_x % SQUARE_SIZE, mouse_y % SQUARE_SIZE)
                        board[row][col] = '.'  # Remove piece from the board temporarily

            # Mouse Button Up - Drop the Piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_piece and current_turn == 'white':  # Only allow white pieces to move
                    mouse_x, mouse_y = event.pos
                    col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                    old_row, old_col = dragging_piece_pos
                    # Drop the piece on the new square
                    if rules(old_row, old_col, row, col, dragging_piece):
                        board[row][col] = dragging_piece
                        dragging_piece = None
                        # Switch turns
                        current_turn = 'black'
                        # AI makes a move after the player
                        make_knowledge_based_move('b')
                        current_turn = 'white'  # Switch back to the player's turn
                    else:
                        board[old_row][old_col] = dragging_piece
                        dragging_piece = None

        # Draw Board and Pieces
        draw_board()
        draw_pieces()

        # Draw Captured Pieces
        draw_captured_pieces()

        # Draw Dragging Piece
        if dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(PIECE_IMAGES[dragging_piece],
                        (mouse_x - dragging_piece_offset[0], mouse_y - dragging_piece_offset[1]))

        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()