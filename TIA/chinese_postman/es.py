import math
import json
import random
import time
import argparse

PROBLEM_FILE = 'grafo_reducido.json'


# Loading problem data
def cargar_datos(datos):
    def jsonKeys2int(x):
        if isinstance(x, dict):
            return {int(k): v for k, v in x.items()}
        return x

    with open(datos, 'r') as r:
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

        threshold = sum([i[2] for i in edges.values()])

        return edges, adjacency, fathers_of, degree, streets, threshold


def condicion_parada():
    if fitness(s_mejor) <= threshold or iteration >= max_iterations:
        return True
    else:
        return False


def crear_vecinos(s_actual, n_vecinos=5, n_max=100):
    vecinos = []
    n_intentos = 0
    while(len(vecinos) < n_vecinos and n_intentos <= n_max):
        # Crear soluciones heuristicas de todas las posiciones
        connections = degree.copy()
        pos = random.choice(range(len(s_actual)))
        individual = s_actual[:pos + 1]
        non_visited_streets = set(streets).difference(individual)
        most_connected = individual[-1]
        for pos in individual:
            for father in fathers_of[pos]:
                connections[father] -= 1
        while not factible(individual) and len(individual) < max_len:
            next_street_posib = adjacency[most_connected]
            # Node with no way posible
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

            individual.append(most_connected)

            # Find out parents and take 1 to the degree
            for father in fathers_of[most_connected]:
                connections[father] -= 1
            non_visited_streets = non_visited_streets.difference([most_connected])

        if factible(individual):
            n_intentos = 0
            vecinos.append(individual)
        else:
            n_intentos += 1

    return vecinos


def crear_vecinos_random(s_actual, n_vecinos=1, n_max=100):
    vecinos = []
    n_intentos = 0
    while(len(vecinos) < n_vecinos and n_intentos <= n_max):
        # Crear vecinos
        pos = random.choice(range(len(s_actual)))
        individual = s_actual[:pos + 1]
        non_visited_streets = set(streets).difference(individual)
        next = individual[-1]
        while not factible(individual) and len(individual) < max_len:
            next_street_posib = adjacency[next]
            next = None
            # Find out which one is the shortest non visited path
            for street in next_street_posib:
                if street in non_visited_streets:
                    next = street
            # For this iteration we have visited all the posibilities
            if next is None:
                next = random.choice(next_street_posib)
            individual.append(next)
        if factible(individual):
            n_intentos = 0
            vecinos.append(individual)
        else:
            n_intentos += 1
            vecino = crear_vecinos(individual, n_vecinos=1)[0]
            vecinos.append(vecino)
    return vecinos


def fitness(individuo):
    if not factible(individuo):
        return math.inf
    else:
        dist = 0
        for i in range(len(individuo)):
            dist += edges[individuo[i]][2]
        return dist


def factible(individual):
    secuencia = True
    if edges[individual[0]][0] != 'A':
        secuencia = False
    if edges[individual[-1]][1] != 'A':
        secuencia = False
    for i in range(len(individual) - 1):
        if edges[individual[i]][1] != edges[individual[i + 1]][0]:
            secuencia = False
    return secuencia and len(set(individual)) == len(streets)


def actualizar_temperatura(iteration, temperatura_actual):
    if args.temp_type == '1':
        return actualizar_temperatura_1(iteration, temperatura_actual)
    elif args.temp_type == '2':
        return actualizar_temperatura_2(iteration, temperatura_actual)
    else:
        return actualizar_temperatura_3(iteration, temperatura_actual)


def actualizar_temperatura_1(iteration, temperatura_actual):
    return t_inicial - iteration * k


def actualizar_temperatura_2(iteration, temperatura_actual):
    return k * temperatura_actual


def actualizar_temperatura_3(iteration, temperatura_actual):
    return t_inicial / (1 + k * temperatura_actual)


# User arguments
parser = argparse.ArgumentParser(description='Process parameters')
parser.add_argument('--k', type=float, default=0.9)
parser.add_argument('--t_inicial', type=int, default=40000)
parser.add_argument('--max_iterations', type=int, default=800)
parser.add_argument('--population_type', type=str, default='heuristics')
parser.add_argument('--temp_type', type=str, default='2')
args = parser.parse_known_args()[0]


# Parametros del sistema
coordenadas = []
datos = PROBLEM_FILE
edges, adjacency, fathers_of, degree, streets, threshold = cargar_datos(datos)
t_inicial = args.t_inicial
k = args.k
s_inicial = [12, 326, 27, 83, 228, 76, 33, 230, 128, 80, 158, 226, 35, 284, 231, 171, 553, 79, 138, 359, 225, 2, 89, 377, 55, 151, 37, 330, 134, 259, 235, 288, 364, 392, 473, 603, 93, 475, 21, 551, 26, 58, 236, 305, 130, 159, 262, 336, 289, 389, 366, 428, 90, 417, 470, 544, 497, 598, 622, 550, 24, 627, 53, 101, 36, 306, 160, 280, 137, 335, 263, 368, 478, 91, 434, 240, 415, 395, 543, 472, 599, 649, 601, 25, 1, 71, 554, 103, 81, 180, 135, 281, 165, 413, 339, 384, 238, 360, 261, 316, 442, 451, 45, 547, 575, 18, 498, 624, 630, 146, 552, 56, 178, 78, 111, 309, 237, 340, 411, 291, 435, 256, 167, 464, 372, 590, 393, 495, 548, 602, 74, 625, 0, 28, 121, 555, 132, 208, 232, 181, 166, 436, 286, 312, 342, 460, 270, 540, 396, 564, 373, 605, 140, 403, 97, 576, 49, 631, 168, 477, 50, 8, 229, 107, 210, 282, 186, 313, 363, 341, 440, 385, 269, 516, 418, 476, 42, 455, 145, 549, 632, 177, 72, 578, 96, 573, 606, 150, 9, 254, 114, 383, 212, 344, 512, 315, 416, 439, 361, 293, 484, 245, 527, 67, 456, 172, 583, 224, 634, 246, 561, 275, 23, 607, 176, 38, 355, 136, 314, 388, 329, 115, 419, 510, 271, 567, 445, 529, 118, 480, 148, 610, 272, 577, 57, 200, 17, 457, 199, 636, 287, 345, 531, 169, 501, 40, 422, 592, 448, 612, 318, 489, 350, 5, 174, 640, 380, 126, 31, 192, 459, 227, 59, 274, 633, 214, 387, 319, 504, 120, 536, 296, 563, 346, 566, 423, 614, 351, 41, 427, 61, 300, 10, 297, 581, 154, 104, 143, 482, 182, 215, 420, 535, 250, 13, 369, 519, 488, 348, 615, 397, 585, 251, 32, 202, 63, 356, 156, 179, 119, 524, 637, 320, 532, 185, 290, 424, 635, 255, 141, 438, 325, 15, 402, 73, 617, 426, 47, 586, 279, 122, 588, 349, 645, 508, 218, 481, 170, 537, 302, 65, 400, 19, 507, 195, 533, 201, 48, 611, 277, 69, 502, 69, 507, 194, 524, 641, 408, 220, 545, 501, 44, 501, 36, 324, 646, 547, 591, 416, 430, 139, 398, 613, 332, 176, 33, 243, 485, 252, 67, 465, 375, 20, 532, 185, 283, 208, 241, 429, 123, 620, 508, 200, 5, 173, 615, 382, 182, 218, 492, 444, 507, 199, 646, 549, 631, 152, 59, 257, 186, 307, 178, 92, 463, 327, 56, 192, 461, 288, 362, 320, 545, 502, 61, 305, 127, 72, 596, 527, 50, 21, 565, 394, 504, 100, 17, 466, 408, 208, 247, 598, 613, 330, 144, 502, 71, 569, 491, 413, 348, 610, 261, 309, 249, 645, 501, 40, 402, 59, 262, 330, 127, 65, 408, 201, 49, 637, 300, 18, 489, 358, 224, 630, 141, 438, 326, 33, 248, 606, 172, 578, 88, 352, 67, 462, 315, 424, 633, 224, 646, 531, 165, 419, 516, 417, 458, 200, 2, 85, 289, 382, 195, 527, 73, 607, 176, 26, 59, 256, 172, 590, 392, 472, 586, 296, 556, 152, 72, 591, 403, 87, 332, 192, 460, 261, 305, 126, 47, 583, 224, 631, 169, 501, 26, 73, 620, 501, 48, 624, 630, 146, 558, 218, 482, 179, 103, 75, 2, 95, 537, 316, 436, 288, 372, 576, 41, 434, 233, 201, 27, 98, 607, 195, 548, 601, 48, 622, 570, 512, 302, 72, 599, 649, 611, 277, 73, 624, 632, 180, 141, 434, 228, 82, 214, 388, 344, 507, 179, 118, 485, 256, 173, 611, 277, 73, 601, 32, 200, 5, 169, 519, 491, 417, 459, 246, 566, 408, 218, 495, 536, 290, 402, 50, 10, 289, 393, 481, 169, 519, 481, 156, 185, 293, 488, 342, 470, 537, 300, 17, 458, 201, 40, 422, 581, 168, 476, 40, 419, 519, 477, 50, 24, 641, 402, 61, 320, 529, 103, 94, 519, 498, 607, 194, 524, 637, 324, 625]
max_len = len(s_inicial) * 2
max_iterations = args.max_iterations
s_actual = s_inicial.copy()
s_mejor = s_actual.copy()
f_mejor = fitness(s_mejor)

t = t_inicial
iteration = 0

start = time.time()

if args.population_type == 'random':
    vecinos = crear_vecinos_random(s_actual)
else:
    print('heuristicas')
    vecinos = crear_vecinos(s_actual)

print('Initial solution fitness: ' + str(f_mejor))
print('Optimal solution: ' + str(threshold))

while(len(vecinos) > 0 and not condicion_parada()):
    if iteration % 100 == 0:
        print("ITERATION " + str(iteration))
    s_nuevo = random.choice(vecinos)
    f_actual = fitness(s_actual)
    coordenadas.append((iteration, f_actual))
    f_nuevo = fitness(s_nuevo)
    ganancia = f_actual - f_nuevo
    if(ganancia >= 0):
        s_actual = s_nuevo.copy()
        f_actual = f_nuevo
        if f_actual < f_mejor:
            s_mejor = s_actual.copy()
            f_mejor = f_actual
    else:
        prob_accept = math.exp(ganancia / t)
        prob = random.random()
        if prob < prob_accept:
            s_actual = s_nuevo
    t = actualizar_temperatura(iteration, t)
    iteration += 1
    if args.population_type == 'random':
        vecinos = crear_vecinos_random(s_actual)
    else:
        vecinos = crear_vecinos(s_actual)
# print('Final solution: ' + str(s_mejor))
print('Final solution fitness: ' + str(f_mejor))
print('Iteracion: ' + str(iteration))
print('Temp: ' + str(t))
end = time.time()
print('TIME ' + str(end - start))
