import random
import itertools
import math
import copy
from numpy import flip

MAX_DEPTH = 3

def merge_left(b):
    # merge the board left
    # this is the funcyoin that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                if x == y or x == 0 or y == 0:
                    return True
        return False

    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4] *10
    for i, j in itertools.product(rows, rows):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    g = Game()
    for i in range(11):
        g.add_two_four(b)


def find_highest_value(b):
    # return highest value of the board
    value = 0
    for row in range(0, len(b)):
        for column in (range(0, len(b))):
            if b[row][column] > value:
                value = b[row][column]
    return value

def find_highest_value_location(b, highest_value):
    for row in range(0, len(b)):
        for column in (range(0, len(b))):
            if b[row][column] == highest_value:
                return (row, column)  # Location of highest value, used in rule 3


def count_empyt_squares(b):
    count = 0
    for row in range(0, len(b)):
        for column in (range(0, len(b))):
            if b[row][column] == 0:
                count += 1
    return count

def value_board(b):
    # value a board state
    score = 0
    # score assignments voor elke rule
    s_rule1 = 300    # Punten voor het hoogste getal in de hoek
    s_rule2 = 25     # Gelijke getallen naast elkaar. Voor elk getal die naast elkaar ligt: bonus score
    s_rule3 = 10     # Lege cellen in de tegenovergestelde hoek van het hoogste getal.
    s_rule4 = 15

    # Rule 1: Hoogste getal in een hoek geeft punten.
    highest_value = find_highest_value(b)
    highest_value_location = find_highest_value_location(b, highest_value)
    for row in range(0, len(b), 3):
        for column in (range(0, len(b), 3)):
            if b[row][column] == highest_value:
                score += s_rule1
                break
        if score != 0:
            break

    # Rule 2: Gelijke getallen naast elkaar. Voor elk getal die naast elkaar ligt = +1 score
    for row in range(0, len(b)):
        for column in range(0, len(b)):
            try:
                if b[row][column] != 0 and b[row][column] == b[row][column+1]:  # getallen op de X as naast elkaar
                    score += s_rule2
                if b[row][column] != 0 and b[row][column] == b[row+1][column]:  # getallen op de Y as naast elkaar
                    score += s_rule2
            except(IndexError):
                pass

    # Rule 3: Lege cellen in de tegenovergestelde hoek van het hoogste getal.
    # alle lege cellen rondom de gespiegelde x,y locatie van het hoogste getal verdient punten
    b_m = flip(b).tolist()      # flip het bord horizontaal en verticaal.
    x = highest_value_location[0]
    y = highest_value_location[1]
    if x-1 >= 0:    # heel lelijk, i know
        if b_m[x-1][y] == 0:    # up
            score+=s_rule3
    if x+1 <= 3:
        if b_m[x+1][y] == 0:    # down
            score+=s_rule3
    if y-1 >= 0:
        if b_m[x][y -1] == 0:    # left
            score+=s_rule3
    if y+1 <= 3:
        if b_m[x][y +1] == 0:    # right
            score+=s_rule3

    # Rule 4: Hoge getallen in een hoek is een hogere score
    score += s_rule4 * count_empyt_squares(b)


    return score

def expectimax(b, depth=3):
    # Generate possible board states given a certain depth.
    # possibilities = dict['direction' => [(boardstate, chance, value), ...]]

    if depth==0 or game_state(b) == 'win' :
        return value_board(b), None

    best_move = None
    best_score = 0

    for direction in MERGE_FUNCTIONS.keys():            # Loop over elke mogelijke zet
        state = MERGE_FUNCTIONS[direction](b)           # create board state
        moves = list()
        for row in range(0, len(state)):                # check each empty cell and assign either 2 or 4 as value
            for column in (range(0, len(state))):
                if state[row][column] == 0:
                    temp2 = copy.deepcopy(state)        # deepcopy to avoid changing lists in lists.
                    temp4 = copy.deepcopy(state)        # deepcopy to avoid changing lists in lists.
                    temp2[row][column] = 2
                    temp4[row][column] = 4
                    moves.append(0.9 * expectimax(temp2, depth-1)[0])   # add to list with it's possiblity and value
                    moves.append(0.1 * expectimax(temp4, depth-1)[0])

        try:
            if sum(moves) / len(moves) > best_score:
                best_score = sum(moves) / len(moves)
                best_move = direction
        except ZeroDivisionError:
            pass


    return best_score, best_move


def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def get_expectimax_move(b):
    move = expectimax(b, 2)
    print(move)
    return move[1]
