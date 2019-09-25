import random
import math

"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a 100-element list, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`. This is because size of square is 10x10,
   and mn means m*10 + n. This avoids conversion between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

# The outside edge is marked ?, empty squares are ., black is @, and white is o.
# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11

# 8 directions; note UP_LEFT = -11, we can repeat this from row to row
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

DEPTH = 0


def squares():
    # list all the valid squares on the board.
    # returns a list [11, 12, 13, 14, 15, 16, 17, 18, 21, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]


def initial_board():
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board


def print_board(board):
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10 * row + 1, 10 * row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    print(rep)


# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. # A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move):
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return isinstance(move, int) and move in squares()


def opponent(player):
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE


def find_bracket(square, player, board, direction):
    # find and return the square that forms a bracket with `square` for `player` in the given
    # `direction`
    # returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket


def is_legal(move, player, board):
    # is this a legal move for the player?
    # move must be an empty square and there has to be is an occupied line in some direction
    # any(iterable) : Return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)


# Making moves
# When the player makes a move, we need to update the board and flip all the
# bracketed pieces.


def make_move(move, player, board):
    # update the board to reflect the move by the specified player
    # assuming now that the move is valid
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board


def make_flips(move, player, board, direction):
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction


# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)


def legal_moves(player, board):
    # get a list of all legal moves for player
    # legals means : move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]


def any_legal_move(player, board):
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())


# Putting it all together

# Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy):
    # play a game of Othello and return the final board and score\
    # black_strategy and white strategy are functions that calculate the next move
    board = initial_board()
    current_player = WHITE

    # While valid moves are still available, keep looping turns between players till game is finished
    while not gameover(board):
        print_board("Playing as " + current_player)
        make_move(get_move("s", current_player, board), current_player, board)
        current_player = next_player(board, current_player)

    if score(WHITE, board) == 0:
        print("It is a draw")
    elif score(WHITE, board) > 0:
        print("White has won with a score of: " + str(score(WHITE, board)))
    else:
        print("Black has won with a score of: " + str(score(BLACK, board)))

    print(print_board(board))


def next_player(board, prev_player):
    # Can the next player do a legal move? Return next player if True
    if any_legal_move(opponent(prev_player), board):
        return opponent(prev_player)

    # If next player can't make a move, can the previous player? Return previous player if True
    if any_legal_move(prev_player, board):
        return prev_player

    # Return None if neither player have valid moves left
    return None


def get_move(strategy, player, board):
    # call strategy(player, board) to get a move
    # TODO: Make use of strategy

    return legal_moves(player, board)[random.randint(1, 50) % len(legal_moves(player, board))]


def score(player, board):
    #      Get length of list of all cells that are occupied by player
    #      and subtract length of list of cells that are occupied by opponent of player
    return len([x for x in range(11, 89) if board[x] == player]) - \
           len([x for x in range(11, 89) if board[x] == opponent(player)])


def gameover(board):
    return any_legal_move(WHITE, board) is False and any_legal_move(BLACK, board) is False


def poging2(board, player):
    copy_of_board = board[:]

    for move in legal_moves(player, copy_of_board):
        make_move(move, player, copy_of_board)
        print_board(copy_of_board)
        copy_of_board = board[:]


def negamax(board, player, depth):
    copy_of_board = board[:]

    if depth == 0 or gameover(copy_of_board):
        return score(player, copy_of_board)

    best_score, best_move = -500000, None

    for move in legal_moves(player, copy_of_board):
        make_move(move, player, copy_of_board)
        old_score = best_score
        best_score = max(best_score, -1 * negamax(copy_of_board, opponent(player), depth-1))

        # If best_score is changed, hence not equal to old_score, update best_move
        if old_score != best_score:
            best_move = move

        # Undo move, so others are checked properly
        copy_of_board = board[:]

    print("Returning recursion layer on board state: ")
    print_board(copy_of_board)
    return best_score, best_move


# play(None, None)
b = initial_board()
negamax(b, WHITE, 5)

# Play strategies
