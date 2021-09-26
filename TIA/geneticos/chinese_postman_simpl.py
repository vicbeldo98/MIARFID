import random
import math
from itertools import groupby
'''
Implementation of the Chinese postman problem with genetic algorithms
ASUMPTION: POSTAMN'S OFFICE IS NODE A
COSAS A TENER EN CUENTA:
    - la longitud del individuo solo es la inicial, porque con el cruce ya no sabes nada
    - la mutacion ayuda a encontrar el individuo ideal en menos iteraciones en este ejemplo
TODO:
    -Mirar que pasa cuando la talla del torneo es mayor ( no nos podemos quedar sin población)
    -Heuristica para la población inicial
    -Relajar restricciones del problema (no hace falta que visiten todas todas las calles)
'''
# Problems data
edges = {
    0: ["A", "B", 1],
    1: ["B", "C", 2],
    2: ["C", "D", 3],
    3: ["D", "A", 5],
    4: ["B", "A", 6]
}

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
threshold = 11
max_iterations = 1000
p_mutation = 0.9
min_length_sol = len(streets)
max_length_mult = 1
max_length_sol = max_length_mult * min_length_sol

# Create initial population
population = []


def create_pseudorandom_population():
    for i in range(population_n):
        k = random.randint(min_length_sol, max_length_sol)
        initial_node = random.choice(initial_streets)
        individual = [initial_node]
        i = 1
        available_perm = streets[1:]
        while i < k:
            n_elem = k - i if i + len(available_perm) > k else len(available_perm)
            individual.extend(random.sample(available_perm, n_elem))
            i += n_elem
            available_perm = list(edges.keys())
            available_perm.remove(individual[-1])
        population.append(individual)
    return population


def create_population_heuristics():
    for i in range(population_n):
        k = random.randint(min_length_sol, max_length_sol)
        initial_street = random.choice(initial_streets)
        individual = [initial_street]
        non_visited_streets = set(streets).difference([initial_street])
        print(non_visited_streets)
        print(connection_dict)
        next_street_posib = connection_dict[initial_street]
        # QUEDARTE CON AQUELLA CUYA LISTA EN CONNECTIONS SEA MENOR
        most_connected = None
        len(i) for i in next_street_posib


# Fitness function
def evaluate(individual):
    if not factible(individual):
        return math.inf
    else:
        dist = 0
        for i in range(len(individual)):
            dist += edges[individual[i]][2]
        return dist


def factible(individual):
    secuencia = True
    if edges[individual[0]][0] != 'A':
        secuencia = False
    if edges[individual[len(individual) - 1]][1] != 'A':
        secuencia = False
    for i in range(len(individual) - 1):
        if edges[individual[i]][1] != edges[individual[i + 1]][0]:
            secuencia = False

    return secuencia and len(set(individual)) == len(streets)


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
    for _ in range(int(len(winner_population) / 2)):
        father = random.choice(winner_population)
        mother = random.choice(winner_population)
        common_edges = list(set(father) & set(mother))
        if common_edges != []:
            winner = random.choice(common_edges)
            father_idx = father.index(winner)
            mother_idx = mother.index(winner)
            son_1 = father[0:father_idx] + mother[mother_idx:]
            son_2 = mother[0:mother_idx] + father[father_idx:]
            new_generation.append(son_1)
            new_generation.append(son_2)
    return new_generation


# Mutations in the new generation
def mutate(new_generation):
    if random.choices([True, False], k=1, weights=[p_mutation, 1 - p_mutation])[0]:
        for i in range(len(new_generation)):
            # Passes through all the streets
            if list(set(new_generation[i])) == streets:
                # Repeated times
                if len(new_generation[i]) > len(streets):
                    prob = [new_generation[i].count(j) / len(new_generation[i]) for j in new_generation[i]]
                    calle = random.choices(new_generation[i], k=1, weights=prob)[0]
                    new_generation[i].remove(calle)
                # Once for every street
                else:
                    if(not factible(new_generation[i])):
                        start = new_generation[i][0]
                        slice = new_generation[i][1:]
                        random.shuffle(slice)
                        new_generation[i] = [start] + slice
                new_generation[i] = [j[0] for j in groupby(new_generation[i])]
            # Does not pass though every street
            else:
                non_visited = list(set(streets).difference(set(new_generation[i])))
                calle_aleatoria = random.choice(non_visited)
                new_generation[i].append(calle_aleatoria)


# Choose next generation individuals
def replacement(population, fitness, population_n):
    # Me quedo los n mejores
    s_fitness, s_popu = zip(*sorted(zip(fitness, population)))
    return list(s_popu)[:population_n + 1], list(s_fitness)[:population_n + 1]


# Stop condition
def stop_condition(fitness, threshold, iteration, max_iterations):
    if fitness[0] <= threshold or iteration > max_iterations:
        return True
    else:
        return False


#   population = create_pseudorandom_population()
population = create_population_heuristics()
'''
fitness = []
for i in population:
    fitness.append(evaluate(i))

iteration = 0
while not stop_condition(fitness, threshold, iteration, max_iterations):
    if(iteration % 100) == 0:
        print(iteration)
    # print('ITERATION: ' + str(iteration))
    # print(population)
    # print(fitness)
    winners, fitness_winners = selection(population, fitness, tournament_n)
    # print('SELETION: ' + str(population))
    new_generation = cross(winners)
    # print('NEW GENERATION: ' + str(new_generation))
    mutate(new_generation)
    # print('MUTAR: ' + str(new_generation))
    new_fitness = []
    for i in new_generation:
        new_fitness.append(evaluate(i))
    winners.extend(new_generation)
    fitness_winners.extend(new_fitness)
    population, fitness = replacement(winners, fitness_winners, population_n)
    iteration += 1

    # input("Press Enter to continue...")

print(population)
print('Best solution: ' + str(population[0]))
print('Fitness: ' + str(fitness[0]))
'''
