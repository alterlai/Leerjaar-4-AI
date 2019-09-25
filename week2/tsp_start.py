import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from collections import namedtuple

# based on Peter Norvig's IPython Notebook on the TSP

City = namedtuple('City', 'x y')

def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)

def try_all_tours(cities):
    # generate and test all possible tours of the cities and choose the shortest tour
    tours = alltours(cities)
    return min(tours, key=tour_length)

def NN(cities):
    # Nearest neighbor algoritme.

    # Pick a random starting point
    cities = set(cities)
    current_city = cities.pop()

    shortest_distance = math.inf     # hoge shortest distance.
    path = [current_city, ]
    closest_city = None
    while len(cities) > 0:
        for city in cities:
            if distance(current_city, city) < shortest_distance:
                shortest_distance = distance(current_city, city)
                closest_city = city
        cities.remove(closest_city)
        path.append(closest_city)
        current_city = closest_city
        shortest_distance = math.inf        # reset shortest distance

    path = two_opt_intersect(path)                           # Perform 2-opt algorithm on path
    return path

def alltours(cities):
    # return a list of tours (a list of lists), each tour a permutation of cities,
    # and each one starting with the same city
    # cities is a set, sets don't support indexing
    start = next(iter(cities)) 
    return [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]

def tour_length(tour):
    # the total of distances between each pair of consecutive cities in the tour
    return sum(distance(tour[i], tour[i-1]) 
               for i in range(len(tour)))

def make_cities(n, width=1000, height=1000):
    # make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed() # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return frozenset(City(random.randrange(width), random.randrange(height))
                     for c in range(n))

def plot_tour(tour): 
    # plot the cities as circles and the tour as lines between them
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()

def plot_tsp(algorithm, cities):
    # apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.clock()
    tour = algorithm(cities)
    t1 = time.clock()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)


# Code van user Grumdrig gebruikt van de volgende link.
# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

# Code van user Grumdrig gebruikt van de volgende link.
# https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def two_opt_swap(path, i, k):
    new_route = path[0:i:]
    new_route += path[k:i:-1]
    new_route += path[k::]
    return new_route

def two_opt_intersect(path):
    best_path = path
    stop = False
    print("starting path length: ", tour_length(best_path))
    print("path nodes: ", len(best_path))
    test = best_path[0]
    while (stop == False):
        new_path = list()
        stop = True
        for i in range(0, len(best_path)):           # Loop over elke node
            for j in range(i+1, len(best_path)):     # zoek vanaf de volgende node na i
                if intersect(best_path[i],best_path[i+1],best_path[j],best_path[j+1]):      # Pad i intersect met pad j
                    new_path.append(best_path[i])          # voeg de node toe aan de new_path
                    new_path.extend(best_path[j:i:-1])     # voeg de lijnen tussen de kruising in reverse order toe
                    new_path.extend(best_path[j+1::])      # voeg de rest van de path toe in normale volgorde
                    best_path = new_path
                    print("new path length: ", tour_length(new_path))
                    print("path nodes: ", len(path))
                    stop = False
                    continue
                else:   # pad intersect niet mer andere paden
                    new_path.append(best_path[i])
                    break
    return best_path


def two_opt(path):
    print(path)
    existing_path = path
    stop = False

    while(stop == False):
        print("Best distance: ", tour_length(existing_path))
        best_distance = tour_length(existing_path)

        # Loop over alle paden
        for i in range(0, len(existing_path) -1):
            for k in range(i + 1, len(existing_path)):
                new_path = two_opt_swap(existing_path, i, k)
                new_distance = tour_length(new_path)
                if new_distance < best_distance:
                    best_distance = new_distance
                    existing_path = new_path
                    print("Best distance: ", tour_length(existing_path))
                    print(len(existing_path))
                    continue
        stop = True
    return existing_path



cities = make_cities(500)
# plot_tsp(try_all_tours, cities)
plot_tsp(NN, cities)

# 1B)
# Hoe langdoet hetNN-programmaover een route met 500 steden en wat is de totale lengte van de route?
# 500 city tour with length 20485.6 in 0.058 secs for NN

# 1C)
# Niet 1 vast aantal. Verschilt per gegenereerde plattegrond.