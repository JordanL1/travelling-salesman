import math
import random
import time
from itertools import permutations

def getShortestRoutes(city_map):
    """ Given a map of city names/IDs, search through every valid tour and return the shortest
    route(s) found.
    """
    routes = getPermutations2(getCityIDs(city_map))
    minCost = getRouteCost(routes[0], city_map)
    minRoutes = [routes[0]]

    for r in routes:
        cost = float(getRouteCost(r, city_map))
        if cost < minCost:
            minCost = cost
            minRoutes = [r]
        elif cost == minCost:
            if r not in minRoutes:
                minRoutes.append(r)

    print(f"Total permutations: {len(routes)}")
    print(f"Minimum route cost: {minCost}")
    print(f"Shortest routes: {minRoutes}")

    return minRoutes

def getShortestRoutesTimed(city_map, time_limit):
    """ Given a map of city names/IDs and a time limit (seconds), search randomly through possible
    tours until the time limit has elapsed, then return the shortest route found.
    """
    finish_time = time.time() + time_limit
    iterations = 0
    route = get_random_route_permutation(getCityIDs(city_map))
    minCost = getRouteCost(route, city_map)
    minRoutes = [route]

    while time.time() < finish_time:
        iterations += 1
        route = get_random_route_permutation(getCityIDs(city_map))
        cost = getRouteCost(route, city_map)

        if cost < minCost:
            minCost = cost
            minRoutes = [route]
        elif cost == minCost:
            if route not in minRoutes:
                minRoutes.append(route)

    print(f"Permutations checked: {iterations}")
    print(f"Minimum route cost: {minCost}")
    print(f"Shortest routes: {minRoutes}")

    return minRoutes

def getRouteCost(route, city_map):
    """ Given a route of city names/IDs as a tuple, and a map of names/IDs to
    coordinates, find the total distance to visit each city in order and return
    to start.
    """
    total = 0.0

    for i in range(0, len(route)-1):
        city = city_map[route[i]]
        nextCity = city_map[route[i+1]]
        distance = getDistance(city, nextCity)
        total += distance

    # Add distance from last city back to first
    lastCity = city_map[route[-1]]
    firstCity = city_map[route[0]]
    total += getDistance(lastCity, firstCity)

    return total

def getPermutations(current, remaining):
    """ Recursive function to get all permutations of a set of values, given the beginning
    sequence of the permutations and the remaining possible values.
    """
    perms = []

    for r in remaining:
        new_remaining = list(remaining)
        new_remaining.remove(r)
        new_current = list(current)
        new_current.append(r)
        perms += getPermutations(new_current, new_remaining)

    if (len(remaining) == 0):
        return [current]
    return perms

def getPermutations2(cities):
    return list(permutations(cities))

def get_random_route_permutation(cities):
    return random.sample(cities, len(cities))

def getCitiesFromFile(fileName):
    """ Given a CSV filename, return a dictionary mapping a city name or ID
    to a tuple containing its 2D coordinates.
    NOTE: Skips the first two lines, assuming they are headers.
    """
    csv = open(fileName, 'r')
    next(csv)
    next(csv)
    cities = {}
    for line in csv:
        city = line.rstrip().split(",")
        cities[city[0]] = (float(city[1]), float(city[2]))    
    print("Cities: " + str(cities))
    return cities

def getDistance(coordA, coordB):
    """ Calculate the distance between two coordinates.
    """
    return math.sqrt((coordB[0] - coordA[0])**2 + (coordB[1] - coordA[1])**2)

def getCityIDs(cities):
    """ Given a map of city IDs/names to coordinates, return a list of cities.
    """
    return list(cities.keys())

getShortestRoutesTimed(getCitiesFromFile("cities18_9.csv"), 3)