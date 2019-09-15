"""
wolf + geit = x
geit + kool = x
Representatie van het probleem:
"""


def dfs(state, path=list()):
    path = path + [state]

    # Als dit een oplossing is, voeg die toe aan de solutions
    if is_goal(state):
        return [path]

    paths = []

    for child in get_available_moves(state):
        print("Now in state: " + child)
        if not visited(path, child):
            newpaths = dfs(child, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def get_available_moves(state):
    # Lijst met mogelijke opvolgende states
    possible_states = []

    # Huidige state gesplits in links en rechts
    actors_left, actors_right = get_left_right(state)

    # Als de boer links zit, ga actors samen met de boer naar de overkant verplaatsen
    if 'B' in actors_left:
        print("\nBoer zit links")
        left, right = get_left_right(state)

        for actor in actors_left:

            # De boer moet altijd verplaatst worden
            left = left.replace('B', '')
            right += 'B'
            print("Boer naar rechts verplaatst")

            if actor != 'B':
                print(actor + " wordt nu verplaatst naar rechts")
                left = left.replace(actor, '')
                right += actor

            # Check of nieuwe tijdelijke state iets oplevert
            print("Tijdelijke nieuwe state: " + left + '|' + right)
            if check_validity(left + '|' + right):
                print("State is valide")
                possible_states += [left + '|' + right]
                print("possible states zijn nu: " + str(possible_states))

            # Reset tijdelijke left, right state
            left, right = get_left_right(state)
            print("Tijdelijke state gereset naar: " + left + "|" + right)

    elif 'B' in actors_right:
        print("\nBoer zit rechts")
        left, right = get_left_right(state)

        for actor in actors_right:
            # De boer wordt altijd verplaatst, dus die skippen we

            # De boer moet altijd verplaatst worden
            right = right.replace('B', '')
            left += 'B'
            print("Boer naar links verplaatst")

            # Als de te verplaatsen actor de B is, dan is deze hierboven al verplaatst
            if actor != 'B':
                print(actor + " wordt nu verplaatst naar links")
                right = right.replace(actor, '')
                left += actor

            # Check of nieuwe tijdelijke state iets oplevert
            print("Tijdelijke nieuwe state: " + left + '|' + right)
            if check_validity(left + '|' + right):
                print("State is valide")
                possible_states += [left + '|' + right]
                print("possible states zijn nu: " + str(possible_states))

            # Reset tijdelijke left, right state
            left, right = get_left_right(state)
            print("Tijdelijke state gereset naar: " + left + "|" + right)

    print("Klaar moet zoeken naar opvolgende states")
    print("Valide volgende states zijn: " + str(possible_states))
    return possible_states


# Check of de state voldoet aan de gestelde regels.
def check_validity(state):
    left, right = get_left_right(state)
    if set(left) == {'G', 'W'} or set(right) == {'G', 'W'}:
        return False
    if set(left) == {'K', 'G'} or set(right) == {'K', 'G'}:
        return False
    return True


def visited(path, child):
    for path_state in path:
        left, right = get_left_right(path_state)
        childleft, childright = get_left_right(child)
        # String omzetten naar een set, zodat deze vergeleken kan worden ongeacht de order
        if set(left) == set(childleft):
            print("State al bezocht, skippen")
            return True
    return False


def is_goal(state):
    # Check of right alle letters bevat
    left, right = get_left_right(state)
    if set(right) == {'B', 'G', 'W', 'K'}:
        return True
    return False


# Zet de string om in left, right variabelen.
def get_left_right(state):
    left, right = state.split("|")
    return left, right


begin_state = 'WKGB|'
# dfs(begin_state, visited, solutions)

solutions = dfs(begin_state)
for solution in solutions:
    print("Solution: ", solution)
