import string
import random

# Boggle
# Kies start positie -> haal lijst op van alle woorden die beginnen met die letter -> maak tree op basis van die letters
# bepaal lengte van langste woord, zodat je stopt met zoeken
# Doe DFS op tree

BORD_SIZE = 5
valid_words = []
solutions = []
visited = []
custom_bord = {0: 'A', 1: 'C', 2: 'X', 3: 'V', 4: 'W', 5: 'A', 6: 'O', 7: 'K', 8: 'J', 9: 'L', 10: 'N', 11: 'B',
               12: 'Y', 13: 'I', 14: 'G', 15: 'Z', 16: 'E', 17: 'L', 18: 'L', 19: 'X', 20: 'K', 21: 'U', 22: 'W',
               23: 'E', 24: 'N'}


def random_letter():
    return random.choice(string.ascii_uppercase)


def generate_bord(n: int):
    bord = dict()
    for x in range(0, n * n):
        bord.update({x: random_letter()})
    return bord


def woordenlijst_maken(valide_woorden):
    f = open("words.txt", "r")
    lines = f.readlines()
    for line in lines:
        line = line.upper()
        valide_woorden.append(line.replace('\n', ''))


def get_adjacent_nodes(node):
    adjacent_nodes = []

    for k, v in letters.items():
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


# Iterate through dictionary that is the board, for each starting letter get the list of available words
def dfs(node, word):
    if word in valid_words:
        solutions.append(word)
        return True

    word = word + node[1]
    visited.append(node)

    for adjacent_node in get_adjacent_nodes(node):
        if adjacent_node not in visited and partial_solution(word + adjacent_node[1]):
            if dfs(adjacent_node, word):
                return True

    return False


def word_from_nodes(nodes):
    str = ''
    for node in nodes:
        str = str + node[1]
    return str


def find_words(node, word_nodes=[]):
    word_nodes = word_nodes + [node]

    if word_from_nodes(word_nodes) in valid_words:
        print("Valid word found: " + word_from_nodes(word_nodes))
        return [word_nodes]

    nodes = []

    for adjacent_node in get_adjacent_nodes(node):

        # If a node hasnt been crossed yet AND the adjacent node still allows for a solution move forward.
        # If false, then ignore that adjacent node
        if adjacent_node not in word_nodes and partial_solution(word_from_nodes(word_nodes) + adjacent_node[1]):
            possible_directions = find_words(adjacent_node, word_nodes)
            for next_node in possible_directions:
                nodes.append(next_node)

    print("Next depth: " + str(nodes))
    return nodes


woordenlijst_maken(valid_words)
letters = custom_bord
print(find_words((0, "A")))
