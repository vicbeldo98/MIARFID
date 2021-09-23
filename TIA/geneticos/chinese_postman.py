import random
# Datos de entrada del problema
# ASUMIMOS QUE EL NODO A ES LA OFICINA DE CORREOS
aristas = {
    0: ["A", "B", 5],
    1: ["A", "C", 2],
    2: ["B", "C", 10],
    3: ["B", "A", 5],
    4: ["C", "B", 1],
    5: ["C", "A", 2],
}
# Definir variables
N = 100
calles = list(aristas.keys())
min_length_sol = len(calles)
max_length_mult = 1
max_length_sol = max_length_mult * min_length_sol

# Crear población inicial
population = []


def create_pseudorandom_population():
    for i in range(N):
        k = random.randint(min_length_sol, max_length_sol)
        individual = [0]
        i = 1
        actual_solution = calles[1:]
        while i < k:
            n_elem = k if i + len(actual_solution) > k else len(actual_solution)
            individual.extend(random.sample(actual_solution, n_elem))
            i += n_elem
            perm = list(aristas.keys())
            perm.remove(actual_solution[-1])
            actual_solution = perm
        if individual[-1] != 0:
            individual.extend([0])
        population.append(individual)
    return population


# Crear población inicial
def create_population_with_heuristic():
    pass


# Crear función fitness
def evaluate(individuo):

    f = factible(individuo)
    if type(f) == int:
        return f
    elif not f:
        return False
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
    if secuencia:
        if len(set(individuo)) == len(calles):
            return True
        else:
            return len(set(individuo)) - len(calles)

    return secuencia and len(set(individuo)) == len(calles)


popluation = create_pseudorandom_population()
print(population)
fitness = []
for i in population:
    fitness.append(evaluate(i))
print(fitness)
