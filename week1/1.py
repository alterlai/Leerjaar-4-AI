"""
wolf + geit = x
geit + kool = x 
"""

solutions = []
visited = list()

def dfs(state, visited):

	# Als dit een oplssing is, voeg hem toe aan de solutions
	if is_goal(state):
		return state

	visited.add(state)
	for child in get_available_moves(state):
		if child not in visited:
			if dfs(state, visited) is not None:
				return state + [state]
	return None

def get_available_moves(state):
	for actor in state[0]:
		

def check_validity(state):
	pass

def is_goal(state):
	pass

begin_state = [['B','W','G','K'],[]]
get_available_moves(begin_state)
# dfs(begin_state, visited)


#todo:
#- Find available moves
#- Check if valid state