"""
wolf + geit = x
geit + kool = x
Representatie van het probleem:
"""


def dfs(state, path=[]):
    path = path + [state]

    # Als dit een oplssing is, voeg hem toe aan de solutions
    if is_goal(state):
        return [path]

    paths = []

    if get_available_moves(state) is not None:
        for child in get_available_moves(state):
            if child not in path:
                newpaths = dfs(child, path)
                if newpaths is not None:
                    for newpath in newpaths:
                        paths.append(newpath)
        return paths


def get_available_moves(state):
    possible_states = []
    actors_left, actors_right = get_left_right(state)
    for actor in actors_left:
        left, right = get_left_right(state)
        # de boer gaat altijd mee dus die kan geskipt worden
        if actor == 'B':
            continue
        left = left.replace(actor, '')
        right += actor

        # Voeg de boer weer toe aan de andere kant.
        if 'B' in left:
            left = left.replace('B', '')
            right += 'B'

        if check_validity(state):
            possible_states += [left + "|" + right,]
    if len(possible_states) == 0: return None
    return possible_states

# Check of de state voldoet aan de gestelde regels.
def check_validity(state):
    left, right = get_left_right(state)
    if set(left) == {'G', 'W'} or set(right) == {'G', 'W'}:
        return False
    if set(left) == {'K', 'G'} or set(right) == {'K', 'G'}:
        return False
    return True


def is_goal(state):
    # Check of right alle letters bevat
    left, right = get_left_right(state)
    if set(right) == {'B', 'G', 'W', 'K'}:
        return True
    return False

# Zet de string om in left, right variabelen.
def get_left_right(state):
    left, right = state.split("|")
    return(left, right)

begin_state = ('WKGB|')
# dfs(begin_state, visited, solutions)

solutions = dfs(begin_state)
for solution in solutions:
    print("Solution: ", solution)

