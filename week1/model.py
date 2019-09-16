import random
import heapq
import math
import week1.config as cf

# global var
grid = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]


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
        return heapq.heappop(self.elements)[1]


def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get()) / 10 else 0


def get_grid_value(node):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    return grid[node[0]][node[1]]


def set_grid_value(node, value):
    # node is a tuple (x, y), grid is a 2D list [x][y]
    grid[node[0]][node[1]] = value


def search(app, start, goal):
    if app.alg.get() == 'UC':
        ucs(start, goal, app)
    if app.alg.get() == 'A*':
        astar(start, goal, app)
    app.pause()


def ucs(start, goal, app, ):
    # Every queue item has ((node, value), priority) -> value and priority are same, but priority is lost on .get()
    queue = PriorityQueue()
    queue.put((start, 0), 0)
    visited = list()

    while not queue.empty():
        position = queue.get()
        current_node = position[0]
        visited.append(current_node)

        if current_node == goal:
            break

        for adjacent_node in get_adjacent_nodes(current_node, visited):
            if adjacent_node not in visited:
                queue.put((adjacent_node, position[1] + 1),
                          position[1] + 1)  # All vertices are 1 step, so +1 is sufficient
                visited.append(adjacent_node)
                app.plot_line_segment(current_node[0], current_node[1], adjacent_node[0], adjacent_node[1],
                                      color=cf.FINAL_C)
                app.pause()


def astar(start, goal, app):
    # Every queue item has ((node, value), priority)
    queue = PriorityQueue()
    queue.put((start, 0), 0)
    visited = list()

    while not queue.empty():
        position = queue.get()
        current_node = position[0]
        visited.append(current_node)

        if current_node == goal:
            break

        for adjacent_node in get_adjacent_nodes(current_node, visited):
            if adjacent_node not in visited:
                # All vertices are 1 step, so +1 is sufficient. Heuristic is 50 (SIZE*2) minus x and y coordinates
                queue.put((adjacent_node, position[1] + 1),
                          cf.SIZE * 2 - adjacent_node[0] - adjacent_node[1])
                visited.append(adjacent_node)
                app.plot_line_segment(current_node[0], current_node[1], adjacent_node[0], adjacent_node[1],
                                      color=cf.FINAL_C)
                app.pause()


def get_adjacent_nodes(node, visited):
    nodes = list()
    valid_nodes = list()
    nodes.append((node[0] + 1, node[1]))
    nodes.append((node[0] - 1, node[1]))
    nodes.append((node[0], node[1] - 1))
    nodes.append((node[0], node[1] + 1))

    for adjacent_node in nodes:
        if adjacent_node[0] in range(cf.SIZE) and adjacent_node[1] in range(cf.SIZE) \
                and get_grid_value(adjacent_node) != 'b' and adjacent_node not in visited:
            valid_nodes.append(adjacent_node)
    return valid_nodes
