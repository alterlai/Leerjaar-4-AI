"""
wolf + geit = x
geit + kool = x
Representatie van het probleem:
"""

solutions = []
visited = []


def dfs(state, visited, solutions):
    # Als dit een oplssing is, voeg hem toe aan de solutions
    if is_goal(state):
        return True


    visited += [state,]
    if get_available_moves(state) is not None:
        for child in get_available_moves(state):
            if child not in visited:
                if dfs(child, visited, solutions):
                    solutions += [child,]
                    return [state, child]

        return False # Als er geen valid move meer is return false


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

        possible_states += [left + "|" + right,]
    if len(possible_states) == 0: return None
    return possible_states

# Check of de state voldoet aan de gestelde regels.
def check_validity(state):
    left, right = get_left_right(state)
    if 'W' in left and 'G' in left or 'W' in right and 'G' in right:
        print(state, "Invalid")
        return False
    if 'G' in left and 'K' in left or 'W' in right and 'G' in right:
        print(state, "valid")
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

dfs(begin_state, visited, solutions)
print(solutions)
