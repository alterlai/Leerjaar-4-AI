import string
import random

# Boggle
# Kies start positie -> haal lijst op van alle woorden die beginnen met die letter -> maak tree op basis van die letters
# bepaal lengte van langste woord, zodat je stopt met zoeken
# Doe DFS op tree

BORD_SIZE = 5
valid_words = list()
solutions = list()
visited = list()
custom_board = {0: 'A', 1: 'C', 2: 'X', 3: 'V', 4: 'W', 5: 'A', 6: 'O', 7: 'K', 8: 'J', 9: 'L', 10: 'N', 11: 'B',
                12: 'Y', 13: 'I', 14: 'G', 15: 'Z', 16: 'E', 17: 'L', 18: 'L', 19: 'X', 20: 'K', 21: 'U', 22: 'W',
                23: 'E', 24: 'N'}


def random_letter():
    return random.choice(string.ascii_uppercase)


def print_board(board: dict):
    board_string = ''
    for k, v in board.items():
        if (k + 1) % BORD_SIZE == 0:
            board_string = board_string + v + '\n'
        else:
            board_string = board_string + v + ' '
    print(board_string)


def generate_board(n: int):
    bord = dict()
    for x in range(0, n * n):
        bord.update({x: random_letter()})
    return bord


def create_valid_word_list():
    f = open("words.txt", "r")
    lines = f.readlines()
    for line in lines:
        line = line.upper()
        valid_words.append(line.replace('\n', ''))


def get_adjacent_nodes(node):
    adjacent_nodes = []

    for k, v in board.items():
        # Check above
        if k == node[0] - 5:
            adjacent_nodes.append((k, v))

        # Check below
        if k == node[0] + 5:
            adjacent_nodes.append((k, v))

        # Check right, if on right outer row, skip
        if k == node[0] + 1 and not (node[0] + 1) % BORD_SIZE == 0:
            adjacent_nodes.append((k, v))

        # Check left
        if k == node[0] - 1 and not node[0] % BORD_SIZE == 0:
            adjacent_nodes.append((k, v))

    return adjacent_nodes


# Checks if the partial word is part of any possible answers
def partial_solution(word):
    for possmatch in valid_words:
        if str(possmatch).startswith(word):
            return True


def word_from_nodes(nodes):
    str = ''
    for node in nodes:
        str = str + node[1]
    return str


def find_words(node, word_nodes=list()):
    word_nodes = word_nodes + [node]
    current_word = word_from_nodes(word_nodes)

    if current_word in valid_words:
        # If a valid word is found, add to solutions
        print("Valid word found: " + current_word)
        solutions.append(current_word)

    if not partial_solution(current_word):
        # If no more solutions available at this point
        # move 1 node back by returning currently list of nodes (which is a valid word)
        return [word_nodes]

    nodes = []

    for adjacent_node in get_adjacent_nodes(node):

        # If a node hasnt been crossed yet AND the adjacent node still allows for a solution move forward.
        # If false, then ignore that adjacent node
        print("Check from node " + str(node[0]) + ": " + node[1])
        print("Checking node " + str(adjacent_node[0]) + ": " + adjacent_node[1])
        if adjacent_node not in word_nodes:
            print("Valid next node!")
            possible_directions = find_words(adjacent_node, word_nodes)
            for next_node in possible_directions:
                nodes.append(next_node)
        print("Node " + str(adjacent_node[0]) + ": " + adjacent_node[1] + " yields no solutions or is already crossed")
    print("Moving back from node " + str(node[0]) + ": " + node[1])

    return nodes


create_valid_word_list()

""""
custom_board layout
A C X V W
A O K J L
N B Y I G
Z E L L X
K U W E N
"""

# Enable either of below to generate a board
# custom_board uses the above layout

board = custom_board
# board = generate_board(5)

# Use print_board to show board in terminal
print_board(board)

for k, v in board.items():
    find_words((k, v))
print(solutions)
