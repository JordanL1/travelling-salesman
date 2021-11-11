import math
import random

FILE_NAME = ""

class Evolutionary:
    POPULATION_SIZE = 100
    SELECTION_SIZE = 30
    RECOMBINATION_PROBABILITY = 1.0
    MUTATION_PROBABILITY = 0.3
    GENERATIONS = 20

    def __init__(self, city_map):
        self.city_map = city_map
        self.cities = list(self.city_map.keys())
        self.population = self.get_initial_population()
        self.best = []
        self.best_cost = 99999

    def solve_TSP(self):
        # Initialise with a random population
        self.population = self.get_initial_population()
        # Print best route in initial pop
        self.get_best_route(self.population)

        for i in range(self.GENERATIONS):
            self.next_generation()
            self.get_best_route(self.population)

        print(f"Best route found is: {self.best} Costing: {self.best_cost}")
        return self.best

    def get_initial_population(self):
        population = []

        for i in range(self.POPULATION_SIZE):
            population.append(self.get_random_route_permutation())

        return population

    def get_best_route(self, routes):
        best = routes[0]
        best_cost = self.get_route_cost(best)

        for route in routes:
            cost = self.get_route_cost(route)

            if cost < best_cost:
                best = route
                best_cost = cost

            if cost < self.best_cost:
                self.best = route
                self.best_cost = cost

        print(f"Best route in current generation is: {best} Costing: {best_cost}")

        return best

    def next_generation(self):
        parents = self.parent_selection_by_tournament()
        offspring = self.produce_offspring(parents)
        self.population = self.survivor_selection_by_elitism(parents, offspring)

    def produce_offspring(self, selected_parents):
        offspring = []

        for i in range(self.POPULATION_SIZE):
            parents = random.sample(selected_parents, 2)
            child = self.order_one_crossover(parents[0], parents[1])

            if random.random() <= self.MUTATION_PROBABILITY:
                child = self.mutate_by_2opt_swap(child)

            offspring.append(child)
        
        return offspring


    def order_one_crossover(self, parent1, parent2):
        start = random.randint(0, len(parent1) - 1)
        end = random.randint(start + 1, len(parent1))
        section = parent1[start:end]

        for city in parent2:
            if city not in section:
                section.append(city)

        return section

    def parent_selection_by_tournament(self):
        selection = []

        for i in range(self.SELECTION_SIZE):
            sublist = random.sample(self.population, int (self.POPULATION_SIZE / 10))
            best = sublist[0]
            best_cost = self.get_route_cost(best)
            
            for route in sublist:
                cost = self.get_route_cost(route)

                if cost < best_cost:
                    best = route
                    best_cost = cost

            selection.append(best)

        return selection    

    def survivor_selection_by_elitism(self, parents, offspring):
        pool = parents + offspring
        pool.sort(key = lambda route : self.get_route_cost(route))

        return pool[0:self.POPULATION_SIZE]

    def mutate_by_2opt_swap(self, route):
        """Given a route, mutate it by selecting a random route from its 2-opt neighbourhood."""
        neighbourhood = self.get_2opt_neighbourhood(route)
        neighbour = random.sample(neighbourhood, 1)[0]

        return neighbour

    def get_2opt_neighbourhood(self, route):
        neighbourhood = []
        neighbourhood.append(route)

        for i in range(0, len(route) - 1):
            for j in range(i+1, len(route)):
                neighbour = route[0:]
                neighbour[i], neighbour[j] = route[j], route[i]
                neighbourhood.append(neighbour)

        return neighbourhood

    def get_route_cost(self, route):
        """ Given a route of city names/IDs as a tuple, and a map of names/IDs to
        coordinates, find the total distance to visit each city in order and return
        to start.
        """
        total = 0.0

        for i in range(0, len(route)-1):
            city = self.city_map[route[i]]
            nextCity = self.city_map[route[i+1]]
            distance = self.get_distance(city, nextCity)
            total += distance

        # Add distance from last city back to first
        lastCity = self.city_map[route[-1]]
        firstCity = self.city_map[route[0]]
        total += self.get_distance(lastCity, firstCity)

        return total

    def get_distance(self, coordA, coordB):
        """ Calculate the distance between two coordinates.
        """
        return math.sqrt((coordB[0] - coordA[0])**2 + (coordB[1] - coordA[1])**2)

    def get_random_route_permutation(self):
        return random.sample(self.cities, len(cities)-1)

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

cities = get_cities_from_file(FILE_NAME)
evol = Evolutionary(cities)
testOffspring = []

for i in range(10):
    testOffspring.append(evol.get_random_route_permutation())