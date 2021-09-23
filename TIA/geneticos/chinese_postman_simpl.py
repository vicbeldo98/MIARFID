import random
import math
# Datos de entrada del problema
# ASUMIMOS QUE EL NODO A ES LA OFICINA DE CORREOS
aristas = {
    0: ["A", "B", 1],
    1: ["B", "C", 2],
    2: ["C", "A", 3],
}
# Definir variables
N = 5
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
def selection(population, fitness, selection_number, tamaño_torneo):
    pass


# Cruzar para obtener una nueva solución
def cruzar(father, mother):
    pass


# Mutar individuo
def mutar(individuo):
    pass


# Ver que individuos me quedaré
def reemplazo(population):
    pass


# Condición de parada
def condicion_parada(population):
    pass


popluation = create_pseudorandom_population()
fitness = []
for i in population:
    fitness.append(evaluate(i))

print(selection(population, fitness, 10))
