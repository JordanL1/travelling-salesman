import random
import math
import time

def local_search(city_map):
    # TODO: Implement random restart
    random_routes = random_search_for_shortest_routes(city_map, 20)
    shortest = random_routes[0]
    shortest_cost = get_route_cost(shortest, city_map)
    print(f"Shortest Random: {shortest} Costing: {shortest_cost}")

    neighbourhood = get_2opt_neighbourhood(shortest)
    shortest_neighbour = get_shortest_in_neighbourhood(neighbourhood, city_map)

    while shortest_neighbour[0] != shortest:
        shortest = shortest_neighbour[0]
        neighbourhood = get_2opt_neighbourhood(shortest)
        shortest_neighbour = get_shortest_in_neighbourhood(neighbourhood, city_map)

    return shortest_neighbour


def local_search_with_random_restart(city_map, time_limit):
    city_list = get_city_IDs(city_map)
    finish_time = time.time() + time_limit
    random_route = get_random_route_permutation(city_list)
    global_shortest = random_route
    global_shortest_cost = get_route_cost(global_shortest, city_map)

    while time.time() < finish_time:
        # Pick and evaluate a random route
        print(f"Picking random route...")
        random_route = get_random_route_permutation(city_list)
        cost = get_route_cost(random_route, city_map)

        if cost < global_shortest_cost:
            global_shortest = random_route
            global_shortest_cost = cost

        # Start iterative neighbourhood search
        print(f"Starting neighbourhood search...")
        neighbourhood = get_2opt_neighbourhood(random_route)
        shortest_neighbour = get_shortest_in_neighbourhood(neighbourhood, city_map)[0]
        shortest_neighbour_cost = get_route_cost(shortest_neighbour, city_map)
        current_shortest = cost

        while shortest_neighbour_cost < current_shortest:
            print(f"Stepping to next neighbour...")
            if shortest_neighbour_cost < global_shortest_cost:
                global_shortest = shortest_neighbour
                global_shortest_cost = shortest_neighbour_cost

            current_shortest = shortest_neighbour_cost
            neighbourhood = get_2opt_neighbourhood(shortest_neighbour)
            shortest_neighbour = get_shortest_in_neighbourhood(neighbourhood, city_map)[0]
            shortest_neighbour_cost = get_route_cost(shortest_neighbour, city_map)

    print(f"Shortest route: {global_shortest}")
    print(f"Costing: {global_shortest_cost}")
    return global_shortest


def random_search_for_shortest_routes(city_map, run_time):
    finish_time = time.time() + run_time
    city_list = get_city_IDs(city_map)

    min_cost = math.inf
    shortest_routes = []

    while time.time() < finish_time :
        route = get_random_route_permutation(city_list)
        cost = get_route_cost(route, city_map)

        if cost < min_cost:
            min_cost = cost
            shortest_routes = [route]
        elif cost == min_cost:
            if route not in shortest_routes:
                shortest_routes.append(route)

    print(min_cost)
    print(shortest_routes)
    return shortest_routes

def get_2opt_neighbourhood(route):
    neighbourhood = []
    neighbourhood.append(route)

    for i in range(0, len(route) - 1):
        for j in range(i+1, len(route)):
            neighbour = route[0:]
            neighbour[i], neighbour[j] = route[j], route[i]
            neighbourhood.append(neighbour)

    return neighbourhood

def get_shortest_in_neighbourhood(neighbourhood, city_map):
    min_cost = math.inf
    shortest_routes = []

    for route in neighbourhood:
        cost = get_route_cost(route, city_map)

        if cost < min_cost:
            min_cost = cost
            shortest_routes = [route]
        elif cost == min_cost:
            if route not in shortest_routes:
                shortest_routes.append(route)

    print(f"Shortest Neighbour: {shortest_routes} Costing: {min_cost}")

    return shortest_routes

def get_cities_from_file(file_name):
    """ Given a CSV filename, return a dictionary mapping a city name or ID
    to a tuple containing its 2D coordinates.
    NOTE: Skips the first two lines, assuming they are headers.
    """
    csv = open(file_name, 'r')
    next(csv)
    next(csv)
    cities = {}
    for line in csv:
        city = line.rstrip().split(",")
        cities[city[0]] = (float(city[1]), float(city[2]))    
    print("Cities: " + str(cities))
    return cities

def get_route_cost(route, city_map):
    """ Given a route of city names/IDs as a tuple, and a map of names/IDs to
    coordinates, find the total distance to visit each city in order and return
    to start.
    """
    total = 0.0

    for i in range(0, len(route)-1):
        city = city_map[route[i]]
        nextCity = city_map[route[i+1]]
        distance = get_distance(city, nextCity)
        total += distance

    # Add distance from last city back to first
    lastCity = city_map[route[-1]]
    firstCity = city_map[route[0]]
    total += get_distance(lastCity, firstCity)

    return total

def get_distance(coordA, coordB):
    """ Calculate the distance between two coordinates.
    """
    return math.sqrt((coordB[0] - coordA[0])**2 + (coordB[1] - coordA[1])**2)

def get_city_IDs(cities):
    """ Given a map of city IDs/names to coordinates, return a list of cities.
    """
    return list(cities.keys())

def get_random_route_permutation(cities):
    return random.sample(cities, len(cities))