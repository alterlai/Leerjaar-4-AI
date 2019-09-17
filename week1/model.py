import random
import heapq
import math
import config as cf

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # to be use in the A* algorithm
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    # in a min-heap, the keys of parent nodes are less than or equal to those
    # of the children and the lowest key is in the root node
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def get(self):
        return heapq.heappop(self.elements)

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]

# Return alle aanliggende nodes die binnen het bord vallen.
def get_adjacent_nodes(node, visited):
    x, y = node
    candidates = []
    candidates.append((x+1, y))
    candidates.append((x, y+1))
    candidates.append((x-1, y))
    candidates.append((x, y-1))

    neighbors = []  # alle valid neighbors
    for x, y in candidates:
        if x < 0 or x >= cf.SIZE:
            continue
        if y < 0 or y >= cf.SIZE:
            continue
        if grid[x][y] == 'b':
            continue
        if (x,y) in visited:
            continue
        neighbors.append((x,y))
    return neighbors

def UCS(app, start, goal):
    # plot a sample path for demonstration
    queue = PriorityQueue()
    visited = []
    queue.put(start, 1)     # zet de start node in de queue
    weight = 0
    path = [start,]
    while(len(queue.elements) > 0):     # zolang er nog items in de queue zitten:
        current_node = queue.get()      # get the top node from the queue
        visited.append(current_node[1])
        # finish requirement
        if current_node[1] == cf.GOAL:
            print("path found!")
            return

        print("current node:", current_node)
        for neighbor in get_adjacent_nodes(current_node[1], visited):       # vindt de aanliggende nodes
            print("neighbours:", neighbor)
            queue.put(neighbor, current_node[0] - 1)                # Zet de neighbor in de queue met een priority van -1 (?)

        # app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
        #app.plot_node((i, i), 'blue')
        app.pause()

def A_star(app, start, goal):
    for i in range(cf.SIZE-1):
        app.plot_line_segment(i, i, i, i+1, color=cf.FINAL_C)
        app.plot_line_segment(i, i+1, i+1, i+1, color=cf.FINAL_C)
        app.pause()

def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value

def search(app, start, goal, alg):
    if alg == "A*":
        A_star(app, start, goal)
    else:
        UCS(app, start, goal)


