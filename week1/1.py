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
		solutions += (state)

	visited += state[0]
	if get_available_moves(state) is not None:
		for child in get_available_moves(state):
			if child[0] not in visited:
				if dfs(state, visited, solutions):
					return (child, state, solutions)
		return False

def get_available_moves(state):
	available_moves = []
	for actor in state[0]:
		print(actor)

		# skip de boer, deze gaat sowieso mee
		if actor == 'B':
			continue
		# Maak een nieuwe state voor elke mogelijke move
		new_state = (state[0][:], state[1][:])

		# Steek een actor over
		new_state[0].remove(actor)
		new_state[1].append(actor)

		# De boer gaat altijd mee naar de overkant
		new_state[0].remove('B')
		new_state[1].append('B')

		print(new_state)
		print("Valid:", check_validity(new_state))
		available_moves.append((new_state))
	if len(available_moves) == 0: return None
	return available_moves
		

# Check of de state voldoet aan de gestelde regels.
def check_validity(state):
	for location in state:
		if 'W' in location and 'G' in location:
			return False
		if 'G' in location and 'K' in location:
			return False
	return True

def is_goal(state):
	# Compare beide lists als sets om volgorde te negeren.
	if len(state[0]) == 0 and set(state[1]) == (['B', 'W', 'G', 'K']):
		return True
	return False


begin_state = (['B','W','G','K'],[])
dfs(begin_state, visited, solutions)

# dfs(begin_state, visited)
