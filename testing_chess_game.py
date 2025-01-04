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

# Restart Function
def restart():
    global board, captured_white, captured_black, dragging_piece, dragging_piece_pos, dragging_piece_offset, current_turn
    # Reset the chessboard to the initial state
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
    # Clear captured pieces
    captured_white = []
    captured_black = []
    # Reset dragging state
    dragging_piece = None
    dragging_piece_pos = None
    dragging_piece_offset = None
    # Reset turn to white
    current_turn = 'white'

# Draw Restart Button
def draw_restart_button():
    # Button dimensions
    button_x, button_y, button_width, button_height = 620, 520, 160, 50
    # Button rectangle
    pygame.draw.rect(screen, (180, 0, 0), (button_x, button_y, button_width, button_height))
    # Button text
    font = pygame.font.SysFont(None, 30)
    text = font.render("Restart", True, (255, 255, 255))
    screen.blit(text, (button_x + 35, button_y + 10))
    return button_x, button_y, button_width, button_height

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
    # Draw captured white pieces
    for i, piece in enumerate(captured_white):
        x_offset = (i % 4) * (SQUARE_SIZE // 2)
        y_offset = (i // 4) * (SQUARE_SIZE // 2)
        screen.blit(PIECE_IMAGES[piece], (white_x + x_offset, white_y + y_offset))
    # Draw captured black pieces
    for i, piece in enumerate(captured_black):
        x_offset = (i % 4) * (SQUARE_SIZE // 2)
        y_offset = (i // 4) * (SQUARE_SIZE // 2)
        screen.blit(PIECE_IMAGES[piece], (black_x + x_offset, black_y + y_offset))

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

# Check if the King is in Check
def is_king_in_check(color):
    king_pos = None
    # Find the king's position
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece == f'{color}K':
                king_pos = (row, col)
                break
        if king_pos:
            break
    if not king_pos:
        return False  # King not found (should not happen)

    # Check if any opponent piece can attack the king
    opponent_color = 'b' if color == 'w' else 'w'
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.' and piece[0] == opponent_color:
                if rules(row, col, king_pos[0], king_pos[1], piece):
                    return True
    return False

# Checkmate Detection
def is_checkmate(color):
    if not is_king_in_check(color):
        return False  # Not in check, so not checkmate

    # Find the king's position
    king_pos = None
    for row in range(8):
        for col in range(8):
            if board[row][col] == f'{color}K':
                king_pos = (row, col)
                break
        if king_pos:
            break
    if not king_pos:
        return False  # King not found (should not happen)

    # Check if the king can move to a safe square
    for row_diff in [-1, 0, 1]:
        for col_diff in [-1, 0, 1]:
            if row_diff == 0 and col_diff == 0:
                continue  # Skip the current position
            new_row, new_col = king_pos[0] + row_diff, king_pos[1] + col_diff
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if rules(king_pos[0], king_pos[1], new_row, new_col, f'{color}K'):
                    # Simulate the move
                    target_piece = board[new_row][new_col]
                    board[new_row][new_col] = f'{color}K'
                    board[king_pos[0]][king_pos[1]] = '.'
                    # Check if the king is still in check after the move
                    if not is_king_in_check(color):
                        # Undo the move
                        board[king_pos[0]][king_pos[1]] = f'{color}K'
                        board[new_row][new_col] = target_piece
                        return False  # King can escape, not checkmate
                    # Undo the move
                    board[king_pos[0]][king_pos[1]] = f'{color}K'
                    board[new_row][new_col] = target_piece

    # Check if any piece can block or capture the attacking piece
    attacking_pieces = []
    opponent_color = 'b' if color == 'w' else 'w'
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.' and piece[0] == opponent_color:
                if rules(row, col, king_pos[0], king_pos[1], piece):
                    attacking_pieces.append((row, col, piece))

    # If there are multiple attacking pieces, the king must move (no blocking or capturing)
    if len(attacking_pieces) > 1:
        return True  # Double check, king must move (but already checked above)

    # If there's only one attacking piece, check if it can be blocked or captured
    if len(attacking_pieces) == 1:
        attacker_row, attacker_col, attacker_piece = attacking_pieces[0]
        # Check if the attacking piece can be captured
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.' and piece[0] == color:
                    if rules(row, col, attacker_row, attacker_col, piece):
                        # Simulate the capture
                        captured_piece = board[attacker_row][attacker_col]
                        board[attacker_row][attacker_col] = piece
                        board[row][col] = '.'
                        # Check if the king is still in check after the capture
                        if not is_king_in_check(color):
                            # Undo the capture
                            board[row][col] = piece
                            board[attacker_row][attacker_col] = captured_piece
                            return False  # Attacker can be captured, not checkmate
                        # Undo the capture
                        board[row][col] = piece
                        board[attacker_row][attacker_col] = captured_piece

        # Check if the attack can be blocked (only for sliding pieces: rook, bishop, queen)
        if attacker_piece[1] in ['R', 'B', 'Q']:
            # Get the path between the attacker and the king
            path = []
            row_diff = king_pos[0] - attacker_row
            col_diff = king_pos[1] - attacker_col
            row_step = 1 if row_diff > 0 else -1 if row_diff < 0 else 0
            col_step = 1 if col_diff > 0 else -1 if col_diff < 0 else 0
            current_row, current_col = attacker_row + row_step, attacker_col + col_step
            while (current_row, current_col) != king_pos:
                path.append((current_row, current_col))
                current_row += row_step
                current_col += col_step

            # Check if any piece can move to a square in the path to block the attack
            for block_row, block_col in path:
                for row in range(8):
                    for col in range(8):
                        piece = board[row][col]
                        if piece != '.' and piece[0] == color:
                            if rules(row, col, block_row, block_col, piece):
                                # Simulate the block
                                target_piece = board[block_row][block_col]
                                board[block_row][block_col] = piece
                                board[row][col] = '.'
                                # Check if the king is still in check after the block
                                if not is_king_in_check(color):
                                    # Undo the block
                                    board[row][col] = piece
                                    board[block_row][block_col] = target_piece
                                    return False  # Attack can be blocked, not checkmate
                                # Undo the block
                                board[row][col] = piece
                                board[block_row][block_col] = target_piece

    # If no moves can escape the check, it's checkmate
    return True

# Evaluate a Move Based on Heuristics
def evaluate_move(board, color):
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                # Add piece value to the score
                score += PIECE_VALUES[piece[1]] * (1 if piece[0] == color else -1)
    return score

# Knowledge-Based Decision Maker
def make_knowledge_based_move(color):
    global captured_white, captured_black
    best_move = None
    best_score = -math.inf
    best_capture = None
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
                            # Check if it's a capture
                            target_piece = board[new_row][new_col]
                            # Evaluate the move
                            score = evaluate_move(new_board, color)
                            if score > best_score:
                                best_score = score
                                best_move = new_board
                                best_capture = target_piece  # Store the captured piece
    if best_move:
        for row in range(8):
            for col in range(8):
                board[row][col] = best_move[row][col]
        if best_capture and best_capture != '.':
            if 'w' in best_capture:
                captured_white.append(best_capture)
            elif 'b' in best_capture:
                captured_black.append(best_capture)

# Display Checkmate Message and Restart Option
def display_checkmate_message(winner):
    # Create a semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
    screen.blit(overlay, (0, 0))

    # Load a custom font
    font_path = "path/to/your/custom/font.ttf"  # Replace with the path to your custom font file
    try:
        font = pygame.font.Font(font_path, 50)
    except:
        font = pygame.font.SysFont("Arial", 50)  # Fallback to Arial if custom font fails

    # Render the checkmate message
    message = f"Checkmate! {winner} wins."
    text = font.render(message, True, (255, 255, 255))  # White text
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    # Render the "Restart?" text
    restart_text = font.render("Restart?", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(restart_text, restart_rect)

    # Draw Yes and No buttons with rounded corners
    yes_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 50, 100, 50)
    no_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 50, 100, 50)

    # Draw rounded rectangles for buttons
    pygame.draw.rect(screen, (0, 200, 0), yes_button, border_radius=10)  # Green button
    pygame.draw.rect(screen, (200, 0, 0), no_button, border_radius=10)  # Red button

    # Render button text
    yes_text = font.render("Yes", True, (255, 255, 255))
    no_text = font.render("No", True, (255, 255, 255))
    screen.blit(yes_text, (yes_button.x + 25, yes_button.y + 10))
    screen.blit(no_text, (no_button.x + 25, no_button.y + 10))

    pygame.display.flip()

    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if yes_button.collidepoint(mouse_x, mouse_y):
                    return True  # Restart the game
                elif no_button.collidepoint(mouse_x, mouse_y):
                    return False  # Exit the game

# Display Check Alert
def display_check_alert(color):
    font = pygame.font.SysFont(None, 50)
    text = font.render(f"{color.capitalize()} King is in Check!", True, (255, 0, 0))
    screen.blit(text, (610, 400))
    pygame.display.flip()
    pygame.time.delay(1000)  # Display the alert for 1 second

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
                mouse_x, mouse_y = event.pos
                # Restart button logic
                button_x, button_y, button_width, button_height = draw_restart_button()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    restart()
                # Player move logic
                elif current_turn == 'white' and 0 <= mouse_x < 600 and 0 <= mouse_y < 600:  # Only allow white pieces to move
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
                    if rules(old_row, old_col, row, col, dragging_piece):
                        # Capture logic
                        target_piece = board[row][col]
                        if target_piece != '.':
                            if 'w' in target_piece:
                                captured_white.append(target_piece)
                                print(f"Captured white piece: {target_piece}")
                            elif 'b' in target_piece:
                                captured_black.append(target_piece)
                                print(f"Captured black piece: {target_piece}")
                        board[row][col] = dragging_piece
                        board[old_row][old_col] = '.'
                        dragging_piece = None
                        # Check if the king is in check
                        if is_king_in_check('b'):
                            display_check_alert('black')
                        # Switch turns
                        current_turn = 'black'
                        # AI makes a move after the player
                        make_knowledge_based_move('b')
                        # Check if the king is in check
                        if is_king_in_check('w'):
                            display_check_alert('white')
                        # Check for checkmate
                        if is_checkmate('w'):
                            print("Checkmate! Black wins.")
                            if display_checkmate_message('Black'):
                                restart()
                            else:
                                running = False
                        elif is_checkmate('b'):
                            print("Checkmate! White wins.")
                            if display_checkmate_message('White'):
                                restart()
                            else:
                                running = False
                        current_turn = 'white'  # Switch back to the player's turn
                    else:
                        board[old_row][old_col] = dragging_piece
                        dragging_piece = None

        # Draw Board and Pieces
        draw_board()
        draw_pieces()

        # Draw Captured Pieces
        draw_captured_pieces()

        # Draw Restart Button
        draw_restart_button()

        # Draw Dragging Piece
        if dragging_piece:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.blit(PIECE_IMAGES[dragging_piece],
                        (mouse_x - dragging_piece_offset[0], mouse_y - dragging_piece_offset[1]))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()