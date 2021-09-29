import random
import math
from itertools import groupby
import json
'''
Implementation of the Chinese postman problem with genetic algorithms
ASUMPTION: POSTAMN'S OFFICE IS NODE A
COSAS A TENER EN CUENTA:
    - la longitud del individuo solo es la inicial, porque con el cruce ya no sabes nada
    - intentar arreglarlos ayuda a encontrar el individuo ideal en menos iteraciones en este ejemplo
    - Heuristica para la población inicial
    - Relajar restricciones del problema (no hace falta que visiten todas las calles)
'''
# PROBLEM DATA LOADING


def jsonKeys2int(x):
    if isinstance(x, dict):
        return {int(k): v for k, v in x.items()}
    return x


with open('graphs/16901_edges.json', 'r') as r:
    aux = dict(json.load(r))
    edges = jsonKeys2int(aux)


initial_streets = []
connection_dict = {}
for i in edges.keys():
    connection_dict[i] = []
for i in edges.keys():
    if edges[i][0] == "A":
        initial_streets.append(i)
    dest = edges[i][1]
    for j in edges.keys():
        if edges[j][0] == dest:
            connection_dict[i].append(j)


streets = list(edges.keys())

# Parameter definition
population_n = 100
tournament_n = 2
threshold = sum([i[2] for i in edges.values()])
max_iterations = 1000
p_mutation = 0.05
min_length_sol = len(streets)
max_length_mult = 2
max_length_sol = max_length_mult * min_length_sol

# Create initial population
population = []


def create_pseudorandom_population():
    for i in range(population_n):
        k = random.randint(min_length_sol, max_length_sol)
        initial_node = random.choice(initial_streets)
        individual = [initial_node]
        ind_len = 1
        available_perm = streets[1:]
        while ind_len < k:
            n_elem = k - ind_len if ind_len + len(available_perm) > k else len(available_perm)
            individual.extend(random.sample(available_perm, n_elem))
            ind_len += n_elem
            available_perm = list(edges.keys())
            available_perm.remove(individual[-1])
        population.append(individual)
    return population


def create_super_individual():
    initial_street = random.choice(initial_streets)
    individual = [initial_street]
    non_visited_streets = set(streets).difference([initial_street])
    ind_len = 1
    most_connected = initial_street
    while ind_len < max_length_sol:
        next_street_posib = connection_dict[most_connected]
        # Node with no way posible
        if next_street_posib == []:
            break
        most_connected = None
        max_connections = -math.inf
        # Find out which one is the most connected edge
        for street in next_street_posib:
            if street in non_visited_streets and len(connection_dict[street]) > max_connections:
                most_connected = street
                max_connections = len(connection_dict[most_connected])

        # For this iteration we have visited all the posibilities
        if most_connected is None:
            most_connected = random.choice(next_street_posib)
        # If all the streets have been visited and we are in node A
        if len(non_visited_streets) == 0 and edges[individual[-1]][1] == "A":
            break

        individual.append(most_connected)
        non_visited_streets = non_visited_streets.difference([most_connected])
        ind_len += 1
    return individual


def create_heuristics_population():
    population = []
    while (len(population) < population_n):
        initial_street = random.choice(initial_streets)
        individual = [initial_street]
        non_visited_streets = set(streets).difference([initial_street])
        ind_len = 1
        actual_street = initial_street
        while ind_len < max_length_sol:
            if len(non_visited_streets) == 0 and edges[individual[-1]][1] == "A":
                break
            next_street_posib = connection_dict[actual_street]
            # Node with no way posible
            if next_street_posib == []:
                break
            next_street_non_visited = list(filter(lambda x: (x in non_visited_streets), next_street_posib))
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
def selection(population, fitness, tournament_size):
    winners = []
    fitness_winners = []
    i = 0
    while i < len(population):
        size = tournament_size if i + tournament_size < len(population) else len(population)
        competitors = fitness[i:i + size]
        index_winner = min(range(len(competitors)), key=competitors.__getitem__)
        winners.append(population[index_winner + i])
        fitness_winners.append(fitness[index_winner + i])
        i += size
    return winners, fitness_winners


# Cross individuals to get next generation
def cross(winner_population):
    new_generation = []
    individual_n = 0
    while (individual_n < int(len(winner_population) / 2)):
        father = random.choice(winner_population)
        mother = random.choice(winner_population)
        if father != mother:
            common_edges = list(set(father) & set(mother))
            if common_edges != []:
                winner = random.choice(common_edges)
                father_idx = father.index(winner)
                mother_idx = mother.index(winner)
                son_1 = father[0:father_idx] + mother[mother_idx:]
                son_2 = mother[0:mother_idx] + father[father_idx:]
                new_generation.append(son_1)
                new_generation.append(son_2)
            individual_n += 1
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
    if fitness[0] != math.inf:
        print("Best solution: " + str(population[0]))
        print('Fitness: ' + str(fitness[0]))
    # there is no factible individual
    else:
        fitness_non_factible = [math.inf] * len(population)
        for i in range(len(population)):
            individual = population[i]
            if correct_path(individual):
                fitness_non_factible[i] = len(set(individual)) - len(streets)
        min_value = min(fitness_non_factible)
        if min_value == math.inf:
            print('NO SOLUTION FOUND')
        else:
            min_index = fitness_non_factible.index(min_value)
            print("Best non factible solution: " + str(population[min_index]))
            print('Fitness: ' + str(fitness_non_factible[min_index]))
    print('Iteration:' + str(iteration))


# CREATING INITIAL POPULATION
population = create_heuristics_population()
population.append(create_super_individual())

fitness = evaluate(population)

#  MAIN BUCLE OF THE GENETIC ALGORITHM
iteration = 0
while not stop_condition(fitness, threshold, iteration, max_iterations):
    if (iteration % 100) == 0:
        print('ITERARION: ' + str(iteration))
    winners, fitness_winners = selection(population, fitness, tournament_n)
    new_generation = cross(winners)
    mutate(new_generation)
    new_population = winners.copy()
    new_population.extend(new_generation)
    population, fitness = replacement(new_population, population_n)
    iteration += 1

print_solution(population, fitness, iteration)
