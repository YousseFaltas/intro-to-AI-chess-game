import numpy as np

# Piece Values
PIECE_VALUES = {
    'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
    'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000
}

# Define center squares
CENTER_SQUARES = [(3, 4), (3, 5), (4, 4), (4, 5)]

# Piece Square Tables
PIECE_SQUARE_TABLES = {
    'P': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5,  5, 10, 25, 25, 10, 5,  5],
        [0,  0,  0, 20, 20,  0, 0,  0],
        [5, -5, -10,  0,  0, -10, -5,  5],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ],
    'N': [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ],
    'B': [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ],
    'R': [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [0,  0,  0,  5,  5,  0,  0,  0]
    ],
    'Q': [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ],
    'K': [
        [-30,-40,-40,-40,-40,-40,-40,-30],
        [-30,-40,-40,-40,-40,-40,-40,-30],
        [-30,-40,-40,-40,-40,-40,-40,-30],
        [-30,-40,-40,-40,-40,-40,-40,-30],
        [-20,-30,-20, -5, -5,-20,-30,-20],
        [-10, 20, 30, 30, 30, 30, 20,-10],
        [20, 30, 40, 50, 50, 40, 30, 20],
        [20, 30, 40, 50, 50, 40, 30, 20]
    ]
}

def determine_game_phase(board):
    piece_count = np.sum(board != '.')
    if piece_count > 24:
        return 'opening'
    elif piece_count > 16:
        return 'middlegame'
    else:
        return 'endgame'
    
def evaluate_king_safety(board, color):
    safety_score = 0
    opponent = 'b' if color == 'w' else 'w'
    king_pos = find_king_position(board, color)
    if not king_pos:
        return 0  # King not found, should not happen in a valid board state

    # Directions around the king (8 squares)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]

    # King's position
    king_row, king_col = king_pos

    # List of squares around the king
    adjacent_squares = [(king_row + dr, king_col + dc) for dr, dc in directions
                        if 0 <= king_row + dr < 8 and 0 <= king_col + dc < 8]

    # Find all opponent pieces
    opponent_pieces = np.argwhere(board[0] == opponent)

    # Count attackers that can attack the king
    attackers = 0
    for opp_pos in opponent_pieces:
        if rules(opp_pos[0], opp_pos[1], king_row, king_col, board[opp_pos[0], opp_pos[1]]):
            attackers += 1

    safety_score -= attackers * 10  # Each attacker subtracts 10 points

    # Count squares around the king that are under attack by opponent pieces
    threatened_squares = 0
    for square in adjacent_squares:
        sr, sc = square
        for opp_pos in opponent_pieces:
            if rules(opp_pos[0], opp_pos[1], sr, sc, board[opp_pos[0], opp_pos[1]]):
                threatened_squares += 1
                break  # No need to check further pieces for this square

    safety_score -= threatened_squares * 5  # Each threatened square subtracts 5 points

    # Count defenders (player's pieces that can move to adjacent squares)
    defenders = 0
    my_pieces = np.argwhere(board[0] == color)
    for square in adjacent_squares:
        sr, sc = square
        for pos in my_pieces:
            if rules(pos[0], pos[1], sr, sc, board[pos[0], pos[1]]):
                defenders += 1
                break  # No need to check further pieces for this square

    safety_score += defenders * 5  # Each defender adds 5 points

    return safety_score

def evaluate_center_control(board, color):
    score = 0.0
    my_color = color
    opponent_color = 'b' if color == 'w' else 'w'
    
    # Get pieces on center squares
    center_pieces = [board[row, col] for row, col in CENTER_SQUARES]
    
    # Evaluate material on center squares
    for piece in center_pieces:
        if piece != '.':
            if piece[0] == my_color:
                score += PIECE_VALUES[piece[1]]
            elif piece[0] == opponent_color:
                score -= PIECE_VALUES[piece[1]]
    
    # Evaluate attacking pieces on center squares
    for square in CENTER_SQUARES:
        row, col = square
        attacking_pieces = np.argwhere(board[0] == my_color)
        for pos in attacking_pieces:
            if rules(pos[0], pos[1], row, col, board[pos[0], pos[1]]):
                score += PIECE_VALUES[board[pos[0], pos[1]][1]] / 2
        attacking_pieces = np.argwhere(board[0] == opponent_color)
        for pos in attacking_pieces:
            if rules(pos[0], pos[1], row, col, board[pos[0], pos[1]]):
                score -= PIECE_VALUES[board[pos[0], pos[1]][1]] / 2
    
    return score

def calculate_mobility(board, color):
    moves = 0
    my_pieces = np.argwhere(board[0] == color)
    for pos in my_pieces:
        piece = board[pos[0], pos[1]]
        for new_row in range(8):
            for new_col in range(8):
                if rules(pos[0], pos[1], new_row, new_col, piece):
                    moves += 1
    return moves

def evaluate_piece_activity(board, color):
    score = 0
    my_pieces = np.argwhere(board[0] == color)
    for pos in my_pieces:
        piece = board[pos[0], pos[1]]
        score += PIECE_VALUES[piece[1]] / 10  # Adjusted activity score
    return score

def get_pawns(board, color):
    pawns = []
    pawn_symbol = f'{color}P'
    pawn_positions = np.argwhere(board[0] == pawn_symbol)
    for pos in pawn_positions:
        pawns.append((pos[0], pos[1]))
    return pawns

def evaluate_pawn_structure(board, color):
    pawns = get_pawns(board, color)
    if not pawns:
        return 0
    
    files = sorted([pawn[1] for pawn in pawns])
    islands = 1
    for i in range(1, len(files)):
        if files[i] != files[i-1] + 1:
            islands += 1
    
    file_counts = {}
    for pawn in pawns:
        col = pawn[1]
        file_counts[col] = file_counts.get(col, 0) + 1
    
    doubled = sum(count - 1 for count in file_counts.values() if count > 1)
    
    files_set = set(files)
    isolated = 0
    for pawn in pawns:
        col = pawn[1]
        adjacent = set()
        if col > 0:
            adjacent.add(col - 1)
        if col < 7:
            adjacent.add(col + 1)
        if not adjacent & files_set:
            isolated += 1
    
    backward = 0
    if color == 'w':
        direction = -1
        enemy_pawn = 'bP'
    else:
        direction = 1
        enemy_pawn = 'wP'
    for pawn in pawns:
        row, col = pawn
        support_rows = range(row - 1, -1, -1) if color == 'w' else range(row + 1, 8)
        supported = any(board[r, col] == f'{color}P' for r in support_rows)
        if not supported:
            enemy_rows = range(row - 1, -1, -1) if color == 'w' else range(row + 1, 8)
            if any(board[r, col] == enemy_pawn for r in enemy_rows):
                backward += 1
    
    passed = 0
    for pawn in pawns:
        row, col = pawn
        is_passed = True
        step = -1 if color == 'w' else 1
        end = -1 if color == 'w' else 8
        for r in range(row + step, end, step):
            if 0 <= r < 8:
                if board[r, col] == enemy_pawn:
                    is_passed = False
                    break
                if col > 0 and board[r, col - 1] == enemy_pawn:
                    is_passed = False
                    break
                if col < 7 and board[r, col + 1] == enemy_pawn:
                    is_passed = False
                    break
        if is_passed:
            passed += 1
    
    score = (
        -10 * islands
        - 20 * doubled
        - 30 * isolated
        - 40 * backward
        + 50 * passed
    )
    return score

def evaluate_position(board, color):
    board = np.array(board)
    score = 0

    # Material Evaluation
    material = 0
    for piece in np.nditer(board):
        if piece != '.':
            if piece[0] == color:
                material += PIECE_VALUES[piece[1]]
            else:
                material -= PIECE_VALUES[piece[1]]
    score += material

    # Center Control
    center_control = 0
    for row, col in CENTER_SQUARES:
        piece = board[row, col]
        if piece != '.':
            if piece[0] == color:
                center_control += 1
            else:
                center_control -= 1
    score += center_control  # Adjust weight as needed

    # King Safety
    score += evaluate_king_safety(board, color)

    # Pawn Structure
    score += evaluate_pawn_structure(board, color)

    # Piece Activity
    score += evaluate_piece_activity(board, color)

    # Game Phase
    phase = determine_game_phase(board)
    if phase == 'endgame':
        score *= 0.8  # Adjust weights for endgame
    elif phase == 'middlegame':
        score *= 1.0
    else:
        score *= 1.2  # Opening phase favors development

    # Piece Square Tables
    for row in range(8):
        for col in range(8):
            piece = board[row, col]
            if piece != '.':
                piece_type = piece[1]
                table = PIECE_SQUARE_TABLES.get(piece_type, [[0]*8 for _ in range(8)])
                if piece[0] == color:
                    score += table[row][col]
                else:
                    score -= table[7 - row][col]  # Mirror for the opponent

    # Mobility
    my_mobility = calculate_mobility(board, color)
    opp_mobility = calculate_mobility(board, 'b' if color == 'w' else 'w')
    score += my_mobility - opp_mobility  # Adjust the weight as needed
    
    return score


def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player, color):
    if depth == 0:
        return evaluate_position(board, color), None
    
    opponent = 'b' if color == 'w' else 'w'
    
    if maximizing_player:
        max_eval = -np.inf
        best_move = None
        for move in generate_legal_moves(board, color):
            # Make the move
            new_board = make_move(board, move)
            # Recursive call
            evaluation, _ = minimax_alpha_beta(new_board, depth - 1, alpha, beta, False, color)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval, best_move
    else:
        min_eval = np.inf
        best_move = None
        for move in generate_legal_moves(board, opponent):
            # Make the move
            new_board = make_move(board, move)
            # Recursive call
            evaluation, _ = minimax_alpha_beta(new_board, depth - 1, alpha, beta, True, color)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval, best_move


def generate_legal_moves(board, color):
    legal_moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.' and piece[0] == color:
                for new_row in range(8):
                    for new_col in range(8):
                        if rules(row, col, new_row, new_col, piece, board):
                            # Create a copy of the board
                            new_board = [row.copy() for row in board]
                            # Move the piece
                            new_board[new_row][new_col] = new_board[row][col]
                            new_board[row][col] = '.'
                            # Check if the move leaves the king in check
                            if not is_king_in_check(new_board, color):
                                legal_moves.append((row, col, new_row, new_col))
    return legal_moves


def make_move(board, move):
    # Implement move logic to create a new board state
    # This function should return a new board after the move is made
    pass


'''
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
                            score = evaluate_position(new_board, color)
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
'''