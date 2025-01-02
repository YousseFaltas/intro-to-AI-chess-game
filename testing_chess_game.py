import pygame

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
# Draw Side Area Background
def draw_side_area():
    # Draw the side area background
    pygame.draw.rect(screen, SIDE_COLOR, (600, 0, 400, 600))

# Draw Captured Pieces
def draw_captured_pieces():
    # Draw the side area background
    draw_side_area()

    # Position for captured white pieces
    white_x = 610  # X position for white pieces
    white_y = 20   # Y position for white pieces

    # Position for captured black pieces
    black_x = 610  # X position for black pieces
    black_y = HEIGHT // 2 + 20  # Y position for black pieces

    # Draw captured white pieces
    for i, piece in enumerate(captured_white):
        screen.blit(PIECE_IMAGES[piece], (white_x + (i % 4) * (SQUARE_SIZE // 2), white_y + (i // 4) * (SQUARE_SIZE // 2)))

    # Draw captured black pieces
    for i, piece in enumerate(captured_black):
        screen.blit(PIECE_IMAGES[piece], (black_x + (i % 4) * (SQUARE_SIZE // 2), black_y + (i // 4) * (SQUARE_SIZE // 2)))
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

# Check if the king is in check
def is_in_check(board, turn):
    # Find the king's position
    king = 'wK' if turn == 'white' else 'bK'
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                king_pos = (row, col)
                break
        if king_pos:
            break

    if not king_pos:
        return False  # King not found (should not happen in a valid game)

    # Check if any opponent's piece can attack the king
    opponent_pieces = ['bP', 'bR', 'bN', 'bB', 'bQ', 'bK'] if turn == 'white' else ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in opponent_pieces:
                if rules(row, col, king_pos[0], king_pos[1], piece):
                    return True  # King is in check
    return False

# Draw Check Alert
def draw_check_alert():
    font = pygame.font.SysFont('Arial', 36)
    check_text = "Check!"
    text_surface = font.render(check_text, True, (255, 0, 0))  # Red color
    screen.blit(text_surface, (610, 400))  # Position the alert on the side

# Draw Current Turn
def draw_current_turn():
    font = pygame.font.SysFont('Arial', 24)
    turn_text = f"Current Turn: {current_turn.capitalize()}"
    text_surface = font.render(turn_text, True, (0, 0, 0))
    screen.blit(text_surface, (610, 500))  # Adjust the position as needed

# Main Game Loop
def main():
    global captured_white, captured_black, current_turn
    captured_white = []  # Clear captured_white at the start
    captured_black = []  # Clear captured_black at the start
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
                mouse_x, mouse_y = event.pos
                col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                if board[row][col] != '.':  # If there's a piece on the square
                    piece = board[row][col]
                    # Check if the piece belongs to the current player
                    if (current_turn == 'white' and 'w' in piece) or (current_turn == 'black' and 'b' in piece):
                        dragging_piece = board[row][col]
                        dragging_piece_pos = (row, col)
                        dragging_piece_offset = (mouse_x % SQUARE_SIZE, mouse_y % SQUARE_SIZE)
                        board[row][col] = '.'  # Remove piece from the board temporarily

            # Mouse Motion - Dragging the Piece
            elif event.type == pygame.MOUSEMOTION:
                if dragging_piece:
                    mouse_x, mouse_y = event.pos

            # Mouse Button Up - Drop the Piece
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging_piece:
                    mouse_x, mouse_y = event.pos
                    col, row = mouse_x // SQUARE_SIZE, mouse_y // SQUARE_SIZE
                    old_row, old_col = dragging_piece_pos
                    # Drop the piece on the new square
                    if rules(old_row, old_col, row, col, dragging_piece):
                        board[row][col] = dragging_piece
                        dragging_piece = None
                        # Switch turns
                        current_turn = 'black' if current_turn == 'white' else 'white'
                    else:
                        board[old_row][old_col] = dragging_piece
                        dragging_piece = None

        # Draw Board and Pieces
        draw_board()
        draw_pieces()

        # Draw Captured Pieces
        draw_captured_pieces()

        # Draw Current Turn
        draw_current_turn()

        # Draw Dragging Piece
        if dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(PIECE_IMAGES[dragging_piece],
                        (mouse_x - dragging_piece_offset[0], mouse_y - dragging_piece_offset[1]))

        # Check if the king is in check and display an alert
        if is_in_check(board, current_turn):
            draw_check_alert()

        pygame.display.flip()  # Update the display

    pygame.quit()

if __name__ == "__main__":
    main()