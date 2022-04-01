"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move


def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    score = get_score(board)
    if color == 1:
        return score[0] - score[1]
    else:
        return score[1] - score[0]


# Better heuristic value of board
def compute_heuristic(board, color):  # not implemented, optional
    # 1. Consider number of possible moves
    # 2. Check current score
    # 3. Check whether it is corner or on the side. Provide a multiplier for this condition
    size = len(board) - 1
    opponent = 1 if color == 2 else 2
    score = compute_utility(board, color)
    corner = 0
    side = 0

    # opponent's possible moves: -2x multiplier
    opponent_moves = get_possible_moves(board, opponent)

    # possible moves: 3x multiplier
    moves = get_possible_moves(board, color)

    # corner: 5x multiplier
    if board[0][0] == color or board[0][size] == color or board[size][0] == color or board[size][size] == color:
        corner += 1

    # side: 2x multiplier
    for i in range(len(board)):
        for j in range(len(board)):
            if board[0][j] == color or board[i][0] == color or board[i][size] == color or board[size][j] == color:
                side += 1

    heuristic = score + 3 * len(moves) + 5 * corner + 2 * side - 2 * len(opponent_moves)
    return heuristic


# global variable to implement state caching
visited = {}


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching=0):
    # if caching is enabled and board is visited, return directly
    if caching:
        key = tuple(map(tuple, board))
        if key in visited:
            return visited[key]

    # get opponent
    opponent = 2 if (color == 1) else 1

    # get opponent's possible moves
    moves = get_possible_moves(board, opponent)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    min_util = float('inf')
    best_move = None

    for move in moves:

        # play the move and get an updated board
        temp_board = play_move(board, opponent, move[0], move[1])

        # recursive call
        _, util = minimax_max_node(temp_board, color, limit - 1, caching)

        # update
        if util < min_util:
            min_util = util
            best_move = move

        # if caching enabled, mark the board as visited
        if caching:
            key = tuple(map(tuple, temp_board))
            visited[key] = (move, util)

    return best_move, min_util


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible utility
    # if caching is enabled and board is visited, return directly
    if caching:
        key = tuple(map(tuple, board))
        if key in visited:
            return visited[key]

    # get possible moves
    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    max_util = -float('inf')
    best_move = None

    for move in moves:
        # play the move and get an updated board
        temp_board = play_move(board, color, move[0], move[1])

        # recursive call
        _, util = minimax_min_node(temp_board, color, limit - 1, caching)

        # update
        if util > max_util:
            max_util = util
            best_move = move

        # if caching enabled, mark the board as visited
        if caching:
            key = tuple(map(tuple, temp_board))
            visited[key] = (move, util)

    return best_move, max_util


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    visited.clear()
    move, util = minimax_max_node(board, color, limit, caching)
    return move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):

    # if caching is enabled and board is visited, return directly
    if caching:
        key = tuple(map(tuple, board))
        if key in visited:
            return visited[key]

    # get opponents
    opponent = 2 if color == 1 else 1

    # get opponent's possible moves
    moves = get_possible_moves(board, opponent)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    min_util = float('inf')
    best_move = None

    # order the moves for maximum utility possible for opponent
    if ordering:
        moves.sort(key=lambda m: compute_utility(play_move(board, opponent, m[0], m[1]), opponent), reverse=True)

    for move in moves:

        # play the move and get an updated board
        temp_board = play_move(board, opponent, move[0], move[1])

        # recursive call
        _, util = alphabeta_max_node(temp_board, color, alpha, beta, limit - 1, caching, ordering)

        # update
        if util <  min_util:
            min_util = util
            best_move = move

        # if caching enabled, mark the board as visited
        if caching:
            key = tuple(map(tuple, temp_board))
            visited[key] = (move, util)

        # update beta
        beta = min(beta, util)
        if beta <= alpha:
            break

    return best_move, min_util


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):

    # if caching is enabled and board is visited, return directly
    if caching:
        key = tuple(map(tuple, board))
        if key in visited:
            return visited[key]

    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return None, compute_utility(board, color)

    # order the moves according to maximum utility possible
    if ordering:
        moves.sort(key=lambda m: compute_utility(play_move(board, color, m[0], m[1]), color), reverse=True)

    max_util = -float('inf')
    best_move = None

    for move in moves:
        # play the move and get an updated board
        temp_board = play_move(board, color, move[0], move[1])

        # recursive call
        _, util = alphabeta_min_node(temp_board, color, alpha, beta, limit - 1, caching, ordering)

        # update
        if util > max_util:
            max_util = util
            best_move = move

        # if caching enabled, mark the board as visited
        if caching:
            key = tuple(map(tuple, temp_board))
            visited[key] = (move, util)

        # update alpha
        alpha = max(alpha, util)
        if beta <= alpha:
            break

    return best_move, max_util


def select_move_alphabeta(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    visited.clear()
    move, util = alphabeta_max_node(board, color, -float('inf'), float('inf'), limit, caching, ordering)
    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta1
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
