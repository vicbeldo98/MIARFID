import random
import math
from itertools import groupby
import json
import time
import argparse

PROBLEM_FILE = 'grafo_reducido.json'


# Loading problem data
def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(k): v for k, v in x.items()}
    return x


with open(PROBLEM_FILE, 'r') as r:
    aux = dict(json.load(r))
    edges = jsonKeys2int(aux)


initial_streets = []
adjacency = {}
fathers_of = {}
for i in edges.keys():
    adjacency[i] = []
    fathers_of[i] = []
for i in edges.keys():
    origin = edges[i][0]
    dest = edges[i][1]
    if origin == "A":
        initial_streets.append(i)
    for j in edges.keys():
        if edges[j][1] == origin:
            fathers_of[i].append(j)
    for j in edges.keys():
        if edges[j][0] == dest:
            adjacency[i].append(j)

degree = {k: len(v) for k, v in adjacency.items()}

streets = list(edges.keys())

# User arguments
parser = argparse.ArgumentParser(description='Process parameters')
parser.add_argument('--population', type=int, default=100)
parser.add_argument('--tournament', type=int, default=2)
parser.add_argument('--max_iterations', type=int, default=800)
parser.add_argument('--p_mutation', type=float, default=0.05)
parser.add_argument('--population_type', type=str, default='heuristics')
args = parser.parse_known_args()[0]

# Parameter definition
population_n = args.population
tournament_n = args.tournament
threshold = sum([i[2] for i in edges.values()])
max_iterations = args.max_iterations
p_mutation = args.p_mutation
min_length_sol = len(streets)
max_length_sol = 2 * min_length_sol

# Create initial population
population = []


def create_heuristics_population():
    population = []
    while (len(population) < population_n):
        connections = degree.copy()
        initial_street = random.choice(initial_streets)
        individual = [initial_street]
        non_visited_streets = set(streets).difference([initial_street])
        ind_len = 1
        most_connected = initial_street
        # Find out parents and take 1 to the degree
        for father in fathers_of[most_connected]:
            connections[father] -= 1
        while ind_len <= max_length_sol:
            next_street_posib = adjacency[most_connected]
            # Node with no way posible
            if next_street_posib == []:
                break
            most_connected = None
            max_connections = -math.inf

            # Find out which one is the most connected edge
            for street in next_street_posib:
                if street in non_visited_streets and connections[street] > max_connections:
                    most_connected = street
                    max_connections = connections[street]

            # For this iteration we have visited all the posibilities
            if most_connected is None:
                most_connected = random.choice(next_street_posib)

            # If all the streets have been visited and we are in node A
            if len(non_visited_streets) == 0 and edges[individual[-1]][1] == "A":
                break

            individual.append(most_connected)
            # Find out parents and take 1 to the degree
            for father in fathers_of[most_connected]:
                connections[father] -= 1
            non_visited_streets = non_visited_streets.difference([most_connected])
            ind_len += 1
        population.append(individual)
    return population


def create_factible_population():
    population = []
    while (len(population) < population_n):
        initial_street = random.choice(initial_streets)
        individual = [initial_street]
        non_visited_streets = set(streets).difference([initial_street])
        ind_len = 1
        actual_street = initial_street
        while ind_len <= max_length_sol:
            if len(non_visited_streets) == 0 and edges[individual[-1]][1] == "A":
                break
            next_street_posib = adjacency[actual_street]
            # Node with no way posible
            if next_street_posib == []:
                break
            next_street_non_visited = [x for x in next_street_posib if x in non_visited_streets]
            if next_street_non_visited == []:
                actual_street = random.choice(next_street_posib)
            else:
                actual_street = random.choice(next_street_non_visited)
            individual.append(actual_street)
            non_visited_streets = non_visited_streets.difference([actual_street])
            ind_len += 1
        population.append(individual)
    return population


# Fitness function
def evaluate(population):
    fitness = []
    for individual in population:
        if not factible(individual):
            fitness.append(math.inf)
        else:
            dist = 0
            for i in range(len(individual)):
                dist += edges[individual[i]][2]
            fitness.append(dist)
    return fitness


def factible(individual):
    return correct_path(individual) and len(set(individual)) == len(streets)


def correct_path(individual):
    secuencia = True
    if edges[individual[0]][0] != 'A':
        secuencia = False
    if edges[individual[len(individual) - 1]][1] != 'A':
        secuencia = False
    for i in range(len(individual) - 1):
        if edges[individual[i]][1] != edges[individual[i + 1]][0]:
            secuencia = False
    return secuencia


# Select parent individuals: by tournament
def selection(population, fitness, tournament_size, n_winners=round(population_n / 2)):
    if n_winners % 2 != 0:
        n_winners += 1
    winners = []
    fitness_winners = []
    deleted_index = []
    i = 0
    while i < len(population) and n_winners > len(winners):
        size = tournament_size if i + tournament_size + 1 < len(population) else len(population) - i
        competitors = fitness[i:i + size]
        index_winner = min(range(len(competitors)), key=competitors.__getitem__)
        winners.append(population[index_winner + i])
        fitness_winners.append(fitness[index_winner + i])
        deleted_index.insert(0, index_winner + i)
        i += size
        if i == len(population):
            i = 0
            for j in deleted_index:
                del population[j]
                del fitness[j]
            deleted_index = []
    return winners, fitness_winners


# Cross individuals to get next generation
def cross(winner_population):
    parents = winner_population.copy()
    new_generation = []
    while (len(parents) > 0):
        father_pos = random.choice(range(len(parents)))
        father = parents[father_pos]
        del parents[father_pos]
        mother_pos = random.choice(range(len(parents)))
        mother = parents[mother_pos]
        del parents[mother_pos]
        common_edges = list(set(father) & set(mother))
        if common_edges != []:
            edge = random.choice(common_edges)
            father_idx = father.index(edge)
            mother_idx = mother.index(edge)
            son_1 = father[0:father_idx] + mother[mother_idx:]
            son_2 = mother[0:mother_idx] + father[father_idx:]
            new_generation.append(son_1)
            new_generation.append(son_2)
    return new_generation


# Mutations in the new generation
def mutate(new_generation):
    for ind in range(len(new_generation)):
        if random.choices([True, False], k=1, weights=[p_mutation, 1 - p_mutation])[0]:
            # Reciprocal Exchange Mutation
            pos_a = random.randint(0, len(new_generation[ind]) - 1)
            pos_b = random.randint(0, len(new_generation[ind]) - 1)
            aux = new_generation[ind][pos_a]
            new_generation[ind][pos_a] = new_generation[ind][pos_b]
            new_generation[ind][pos_b] = aux


# Choose next generation individuals
def replacement(population, population_n):
    # Try to fix population
    hospital(population)
    # Get the best n
    fitness = evaluate(population)
    s_fitness, s_popu = zip(*sorted(zip(fitness, population)))
    return list(s_popu)[:population_n + 1], list(s_fitness)[:population_n + 1]


def hospital(population):
    for i in range(len(population)):
        if not factible(population[i]):
            if correct_path(population[i]):
                # Does not pass though every street
                non_visited = list(set(streets).difference(set(population[i])))
                calle_aleatoria = random.choice(non_visited)
                population[i].append(calle_aleatoria)
            else:
                # Not even a correct path. Random shuffle
                start = population[i][0]
                slice = population[i][1:]
                random.shuffle(slice)
                population[i] = [start] + slice
            # Delete repeated consecutive edges
            population[i] = [j[0] for j in groupby(population[i])]


# Stop condition
def stop_condition(fitness, threshold, iteration, max_iterations):
    if fitness[0] <= threshold or iteration >= max_iterations:
        return True
    else:
        return False


# Print found solution
def print_solution(population, fitness, iteration):
    print('****************************************')
    print('Sum of all edges(optimal): ' + str(threshold))
    print('Iteration:' + str(iteration))
    if fitness[0] != math.inf:
        print("Best solution: " + str(population[0]))
        print('Fitness: ' + str(fitness[0]))
    # there is no factible individual
    else:
        print('NO SOLUTION FOUND')


start = time.time()

# CREATING INITIAL POPULATION
if(args.population_type == 'random'):
    population = create_factible_population()
else:
    population = create_heuristics_population()

fitness = evaluate(population)

#  MAIN BUCLE OF THE GENETIC ALGORITHM
iteration = 0
while not stop_condition(fitness, threshold, iteration, max_iterations):
    winners, fitness_winners = selection(population, fitness, tournament_n)
    new_generation = cross(winners)
    mutate(new_generation)
    new_population = winners.copy()
    new_population.extend(new_generation)
    population, fitness = replacement(new_population, population_n)
    iteration += 1

print_solution(population, fitness, iteration)

end = time.time()
print('TIME ' + str(end - start))
