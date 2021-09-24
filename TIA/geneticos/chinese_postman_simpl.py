import random
import math
from itertools import groupby
# Datos de entrada del problema
# ASUMIMOS QUE EL NODO A ES LA OFICINA DE CORREOS
aristas = {
    0: ["A", "B", 1],
    1: ["B", "C", 2],
    2: ["B", "D", 3],
    3: ["B", "E", 5],
    4: ["B", "H", 1],
    5: ["C", "D", 1],
    6: ["C", "F", 2],
    7: ["C", "H", 3],
    8: ["D", "G", 5],
    9: ["D", "H", 1],
    10: ["H", "G", 1],
    11: ["G", "F", 2],
    12: ["F", "C", 3],
    13: ["F", "E", 5],
    14: ["E", "A", 1],
}

# Definir variables
population_n = 100
torneo_n = 2
threshold = 12
max_iterations = 1000
calles = list(aristas.keys())
min_length_sol = len(calles)
max_length_mult = 2
max_length_sol = max_length_mult * min_length_sol

# Crear población inicial
population = []


def create_pseudorandom_population():
    for i in range(population_n):
        k = random.randint(min_length_sol, max_length_sol)
        individual = [0]
        i = 1
        available_perm = calles[1:]
        while i < k:
            n_elem = k - i if i + len(available_perm) > k else len(available_perm)
            individual.extend(random.sample(available_perm, n_elem))
            i += n_elem
            available_perm = list(aristas.keys())
            available_perm.remove(individual[-1])
        population.append(individual)
    return population


# Crear función fitness
def evaluate(individuo):
    if not factible(individuo):
        return math.inf
    else:
        dist = 0
        for i in range(len(individuo)):
            dist += aristas[individuo[i]][2]
        return dist


def factible(individuo):
    secuencia = True
    if aristas[individuo[0]][0] != 'A':
        secuencia = False
    if aristas[individuo[len(individuo) - 1]][1] != 'A':
        secuencia = False
    for i in range(len(individuo) - 1):
        if aristas[individuo[i]][1] != aristas[individuo[i + 1]][0]:
            secuencia = False

    return secuencia and len(set(individuo)) == len(calles)


# Seleccionar los individuos que serán padres: por torneo
def selection(population, fitness, tamaño_torneo):
    winners = []
    fitness_winners = []
    i = 0
    while i < len(population):
        size = tamaño_torneo if i + tamaño_torneo < len(population) else len(population)
        competitors = fitness[i:i + size]
        index_winner = min(range(len(competitors)), key=competitors.__getitem__)
        winners.append(population[index_winner + i])
        fitness_winners.append(fitness[index_winner + i])
        i += size
    return winners, fitness_winners


# Cruzar para obtener una nueva solución
def cruzar(winner_population):
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


# Mutar individuo
def mutar(new_generation):
    for i in range(len(new_generation)):
        # Pasa por todas las calles
        if list(set(new_generation[i])) == calles:
            # Por alguna repetidas veces
            if len(new_generation[i]) > len(calles):
                prob = [new_generation[i].count(j) / len(new_generation[i]) for j in new_generation[i]]
                calle = random.choices(new_generation[i], k=1, weights=prob)[0]
                new_generation[i].remove(calle)
            # Una vez por cada una
            else:
                if(not factible(new_generation[i])):
                    slice = new_generation[i][1:]
                    random.shuffle(slice)
                    new_generation[i] = [0] + slice
            new_generation[i] = [j[0] for j in groupby(new_generation[i])]
        # No pasa por todas las calles
        else:
            non_visited = list(set(calles).difference(set(new_generation[i])))
            calle_aleatoria = random.choice(non_visited)
            new_generation[i].append(calle_aleatoria)


# Ver que individuos me quedaré
def reemplazo(population, fitness, population_n):
    # Me quedo los n mejores
    s_fitness, s_popu = zip(*sorted(zip(fitness, population)))
    return list(s_popu)[:population_n + 1], list(s_fitness)[:population_n + 1]


# Condición de parada
def condicion_parada(fitness, threshold, iteration, max_iterations):
    if fitness[0] <= threshold or iteration > max_iterations:
        return True
    else:
        return False


population = create_pseudorandom_population()
fitness = []
for i in population:
    fitness.append(evaluate(i))

iteration = 0
while not condicion_parada(fitness, threshold, iteration, max_iterations):
    if(iteration % 100) == 0:
        print(iteration)
    print('ITERATION: ' + str(iteration))
    print(population)
    print(fitness)
    winners, fitness_winners = selection(population, fitness, torneo_n)
    print('SELETION: ' + str(population))
    new_generation = cruzar(winners)
    print('NEW GENERATION: ' + str(new_generation))
    mutar(new_generation)
    print('MUTAR: ' + str(new_generation))
    new_fitness = []
    for i in new_generation:
        new_fitness.append(evaluate(i))
    winners.extend(new_generation)
    fitness_winners.extend(new_fitness)
    population, fitness = reemplazo(winners, fitness_winners, population_n)
    iteration += 1

    # input("Press Enter to continue...")


print('Best solution: ' + str(population[0]))
