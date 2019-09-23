import random
import heapq
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
    nodes = dict()
    if app.alg.get() == 'UC':
        nodes = ucs(start, goal, app)
    if app.alg.get() == 'A*':
        nodes = astar(start, goal, app)

    # Below code is inspired by Melle Dijkstra
    key = goal
    while key in nodes.keys():
        prev = nodes.get(key)
        app.plot_line_segment(key[0], key[1], prev[0], prev[1], cf.FINAL_C)
        key = prev

    app.pause()


def ucs(start, goal, app):
    # Every queue item has (node, priority)
    queue = PriorityQueue()
    queue.put((start, 0), 0)
    visited = list()
    all_traversed_nodes = dict()

    while not queue.empty():
        position = queue.get()
        current_node = position[0]
        steps_to_current_node = position[1]
        visited.append(current_node)

        if current_node == goal:
            return all_traversed_nodes

        for adjacent_node in get_adjacent_nodes(current_node, visited):
            if adjacent_node not in visited:
                # All vertices are 1 step, so +1 is sufficient
                queue.put((adjacent_node, steps_to_current_node + 1), steps_to_current_node + 1)
                visited.append(adjacent_node)

                # Track node chains -> Thanks to Melle Dijkstra for idea
                all_traversed_nodes.update({adjacent_node: current_node})

                # Replace with nodeblock, line moved to search()
                app.plot_node(adjacent_node, cf.PATH_C)
                app.pause()


def astar(start, goal, app):
    # Every queue item has ((node, value), priority)
    queue = PriorityQueue()
    queue.put((start, 0), 0)
    visited = list()
    all_traversed_nodes = dict()

    while not queue.empty():
        position = queue.get()
        current_node = position[0]
        steps_to_current_node = position[1]
        visited.append(current_node)

        if current_node == goal:
            return all_traversed_nodes

        for adjacent_node in get_adjacent_nodes(current_node, visited):
            if adjacent_node not in visited:
                # All vertices are 1 step, so +1 is sufficient. Heuristic is GOAL x and y minus x and y coordinates
                queue.put((adjacent_node, steps_to_current_node + 1),
                          steps_to_current_node + 1 + get_manhattan_distance(adjacent_node, goal))
                visited.append(adjacent_node)
                all_traversed_nodes.update({adjacent_node: current_node})
                app.plot_node(adjacent_node, color=cf.PATH_C)
                app.pause()


def get_manhattan_distance(start, target):
    return abs(start[0]-target[0]) + abs(start[1]-target[1])


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
