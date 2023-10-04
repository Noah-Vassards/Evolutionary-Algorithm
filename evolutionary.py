from graph import Graph

import random as rd
import itertools as it
from collections import Counter
import time


def generate_permutations(number, l):
    if number == 1:
        return rd.sample(l, len(l))
    permutations = []
    for _ in range(number):
        random_permutation = rd.sample(l, len(l))
        permutations.append(random_permutation)
    return permutations


def get_first_not_in_list(list, elems):
    """_summary_:
        get the first element not in the list

    Args:
        list (list): the list where to check for missing elements
        elems (_type_): the list of elements to check if missing

    Returns:
        _type_: _description_
    """
    for elem in elems:
        if elem not in list:
            return elem


def check_visit_once(iter: list, verticies):
    """_summary_:
        Counts each element in an iterable and replace each multiple occurences
        by vertices not in the iterable

    Args:
        iter (list): an iterable
        verticies (list): all verticies in the graph
    """
    for l in iter:
        visits = Counter(l)
        for key in visits:
            if visits[key] > 1:
                l[l.index(key)] = get_first_not_in_list(l, verticies)


def mutation2(population, graph: Graph):
    for indiv in population:
        print('mutating indiv')
        indiv_len = len(indiv)
        # print('indiv len', indiv_len)
        count = 0
        for i in range(0, indiv_len-3):
            for j in range(i + 2, indiv_len - 2):
                count += 1
                # print((i, i + 1, j, j + 1))
                gain = graph.get_edge_weight((indiv[i], indiv[i + 1])) + graph.get_edge_weight(
                    (indiv[j], indiv[j + 1])) - graph.get_edge_weight((indiv[i], indiv[j])) - graph.get_edge_weight((indiv[i + 1], indiv[j + 1]))
                if gain > 0:
                    indiv[i + 1], indiv[j] = indiv[j], indiv[i + 1]


def mutation(population):
    """_summary_:
        swaps two verticies with each other in each individuals of the 
        population

    Args:
        population (list): a list containing all individuals
    """
    for indiv in population:
        idx1, idx2 = rd.sample(range(0, len(indiv) - 1), 2)
        tmp = indiv[idx1]
        indiv[idx1] = indiv[idx2]
        indiv[idx2] = tmp


def cross_over2(indiv1, indiv2, verticies: list):
    """_summary_:
        creates to new individual by swapping ends from the old individuals.
        Also avoids multiple occurences of vertices by the missing ones

    Args:
        indiv1 (list): the first individual
        indiv2 (list): the second individal
        verticies (list): all vertices of the graph

    Returns:
        list, list: both newly created individuals
    """
    rd_index = rd.randint(1, len(indiv1) - 2)
    tmp = indiv1[rd_index:]
    indiv1[rd_index:] = indiv2[rd_index:]
    indiv2[rd_index:] = tmp
    check_visit_once([indiv1, indiv2], verticies)
    return indiv1, indiv2


def cross_over(indiv1: list, indiv2: list):
    """_summary_:
        creates to new individual by swapping ends from the old individuals

    Args:
        indiv1 (list): the first individual
        indiv2 (list): the second individal

    Returns:
        list, list: both newly created individuals
    """
    rd_index = rd.randint(1, len(indiv1) - 2)
    tmp = indiv1[rd_index:]
    indiv1[rd_index:] = indiv2[rd_index:]
    indiv2[rd_index:] = tmp
    return indiv1, indiv2

def selection3(population: list, pop_fitness: list,
               verticies: list, graph: Graph):
    """_summary_:
        select the best individuals to create a new population with increased
        diversity

    Args:
        population (list): a list containing all individuals
        pop_fitness (list): a list containing the fitness score of each 
                            individual
        verticies (list): all verticies of the graph

    Returns:
        list: the newest population
    """
    drop = population[pop_fitness.index(min(pop_fitness))]
    population.remove(drop)
    population.append(rd.choice(population))
    len_pop = len(population)
    new_pop = []
    for i in range(0, len_pop, 2):
        if i + 1 < len_pop:
            child1, child2 = cross_over2(
                population[i], population[(i + 1)], verticies)
            new_pop.extend([child1, child2])
        else:
            new_pop.append(generate_permutations(1, verticies))
    mutation2(new_pop, graph)
    return new_pop

def selection2(population: list, pop_fitness: list,
               verticies: list, permutations: list, graph: Graph):
    """_summary_:
        select the best individuals to create a new population with increased
        diversity

    Args:
        population (list): a list containing all individuals
        pop_fitness (list): a list containing the fitness score of each 
                            individual
        verticies (list): all verticies of the graph

    Returns:
        list: the newest population
    """
    drop = population[pop_fitness.index(min(pop_fitness))]
    population.remove(drop)
    population.append(rd.choice(population))
    len_pop = len(population)
    new_pop = []
    for i in range(0, len_pop, 2):
        if i + 1 < len_pop:
            child1, child2 = cross_over2(
                population[i], population[(i + 1)], verticies)
            new_pop.extend([child1, child2])
        else:
            new_pop.append(list(rd.choice(permutations)))
    mutation2(new_pop, graph)
    return new_pop


def selection(population: list, pop_fitness: list, verticies: list):
    """_summary_:
        select the best individuals to create a new population

    Args:
        population (list): a list containing all individuals
        pop_fitness (list): a list containing the fitness score of each 
                            individual
        verticies (list): all verticies of the graph

    Returns:
        list: the newest population
    """
    drop = population[pop_fitness.index(min(pop_fitness))]
    population.remove(drop)
    population.append(rd.choice(population))
    len_pop = len(population)
    new_pop = []
    for i in range(0, len_pop, 2):
        if i + 1 < len_pop:
            child1, child2 = cross_over2(
                population[i], population[(i + 1)], verticies)
            new_pop.extend([child1, child2])
        else:
            new_pop.append(population[i])
    mutation(new_pop)
    return new_pop


def fitness4(graph: Graph, population, verticies_nb):
    """_summary_
        compute a fitness score for each individual in a population. Checks for
        each adjacent vertices if the edge exists in the graph and also 
        computes the length of the path. The more adjacent vertices exist and 
        the shorter the path compared with 70% of the graph length, the higher 
        the score.

    Args:
        graph (Graph): Graph structure to parse
        population (list[list]): a list containing every individual of the generation
        verticies_nb (int): number of vertices in the graph

    Yields:
        int: fitness score of an individual
    """
    edges = graph.get_edges()
    score = 0
    graph_length = graph.get_total_len()
    total_length = 0
    for parent in population:
        for i, vertex in enumerate(parent):
            if (vertex, parent[(i + 1) % len(parent)]) not in edges and (parent[(i + 1) % len(parent)], vertex) not in edges:
                total_length = graph_length
                break
            total_length += graph.get_edge_weight(
                (vertex, parent[(i + 1) % len(parent)]))
            score += 1
        yield ((score / verticies_nb) * 50) + int(abs(50 * ((graph_length - total_length) / (0.7 * graph_length))))
        score = 0
        total_length = 0


def fitness3(graph: Graph, population, verticies_nb):
    """_summary_
        compute a fitness score for each individual in a population. Checks for
        each adjacent vertices if the edge exists in the graph and also 
        computes the lenght of the path. The more adjacent vertices exist
        and the shorter the path compared to the total length of the graph, 
        the higher the score.

    Args:
        graph (Graph): Graph structure to parse
        population (list[list]): a list containing every individual of the generation
        verticies_nb (int): number of vertices in the graph

    Yields:
        int: fitness score of an individual
    """
    edges = graph.get_edges()
    score = 0
    graph_length = graph.get_total_len()
    total_length = 0
    for parent in population:
        for i, vertex in enumerate(parent):
            if (vertex, parent[(i + 1) % len(parent)]) not in edges and (parent[(i + 1) % len(parent)], vertex) not in edges:
                total_length = graph_length
                break
            total_length += graph.get_edge_weight(
                (vertex, parent[(i + 1) % len(parent)]))
            score += 1
        yield ((score / verticies_nb) * 50) + int((50 * (graph_length - total_length) / graph_length))
        score = 0
        total_length = 0


def fitness2(graph: Graph, population, verticies_nb):
    """_summary_
        compute a fitness score for each individual in a population. Checks for
        each adjacent vertices if the edge exists in the graph and also for
        any multiple occurrence of a vertex. The more adjacent vertices exist
        and the less multiple occurrence, the higher the score.

    Args:
        graph (Graph): Graph structure to parse
        population (list[list]): a list containing every individual of the generation
        verticies_nb (int): number of vertices in the graph

    Yields:
        int: fitness score of an individual
    """
    edges = graph.get_edges()
    score = 0
    for parent in population:
        visits = Counter(parent)
        for key in visits:
            if visits[key] != 1:
                score -= 1
        for i, vertex in enumerate(parent):
            if (vertex, parent[(i + 1) % len(parent)]) not in edges and (parent[(i + 1) % len(parent)], vertex) not in edges:
                break
            score += 1
        yield (score / verticies_nb) * 100
        score = 0


def fitness(graph: Graph, population, verticies_nb):
    """_summary_
        compute a fitness score for each individual in a population. Checks for
        each adjacent vertices if the edge exists. The more adjacent vertices 
        exist, the higher the score.

    Args:
        graph (Graph): Graph structure to parse
        population (list[list]): a list containing every individual of the generation
        verticies_nb (int): number of vertices in the graph

    Returns:
        None

    Yields:
        int: fitness score of an individual
    """
    edges = graph.get_edges()
    score = 0
    for parent in population:
        for i, vertex in enumerate(parent):
            if (vertex, parent[(i + 1) % len(parent)]) not in edges and (parent[(i + 1) % len(parent)], vertex) not in edges:
                break
            score += 1
        yield (score / verticies_nb) * 100
        score = 0

def evolutionary4(graph: Graph) -> list | str:
    """_summary_:
        Evolutionary algorithm main. Initialize a population then loops until
        a fit enough path is found after a certain number of generations, 
        or if the 1000th generation is reached.

    Args:
        graph (Graph): Graph structure where to look for the shortest path

    Returns:
        str | list: 
            On failure, returns 'failure'
            On success, returns the list containing the path
    """
    count = 0
    start_time = time.time()
    populations = 0
    generation = 10
    max_fitness = 0
    verticies = graph.get_verticies()
    population = generate_permutations(10, verticies)
    print('population ok')
    while True:
        print(count)
        if count > 1000:
            print(f'Elapsed time is 999999999999999999999999ms')
            print(f'Number of populations: 999999999999999999999999')
            return 'failure'
        populations += 1
        print(population)
        pop_fitness = list(fitness4(graph, population, len(verticies)))
        print(pop_fitness)
        if generation <= 0 and max(pop_fitness) >= max_fitness:
            end = time.time() - start_time
            print(f'Elapsed time is {end * 1000:.2f}ms')
            print(f'Number of populations: {populations}')
            return population[pop_fitness.index(max(pop_fitness))]
        population = selection3(population, pop_fitness,
                                verticies, graph)
        generation -= 1
        max_fitness = max(max_fitness, max(pop_fitness))
        count += 1


def evolutionary3(graph: Graph) -> list | str:
    """_summary_:
        Evolutionary algorithm main. Initialize a population then loops until
        a fit enough path is found after a certain number of generations, 
        or if the 1000th generation is reached.

    Args:
        graph (Graph): Graph structure where to look for the shortest path

    Returns:
        str | list: 
            On failure, returns 'failure'
            On success, returns the list containing the path
    """
    count = 0
    start_time = time.time()
    populations = 0
    generation = 5
    max_fitness = 0
    verticies = graph.get_verticies()
    permutations = list(it.permutations(verticies))
    population = rd.sample(permutations, 10)
    population = [list(indiv) for indiv in population]
    while True:
        print(count)
        if count > 1000:
            print(f'Elapsed time is 999999999999999999999999ms')
            print(f'Number of populations: 999999999999999999999999')
            return 'failure'
        populations += 1
        print(population)
        pop_fitness = list(fitness4(graph, population, len(verticies)))
        print(pop_fitness)
        if generation <= 0 and max(pop_fitness) >= max_fitness:
            end = time.time() - start_time
            print(f'Elapsed time is {end * 1000:.2f}ms')
            print(f'Number of populations: {populations}')
            return population[pop_fitness.index(max(pop_fitness))]
        population = selection2(population, pop_fitness,
                                verticies, permutations, graph)
        generation -= 1
        max_fitness = max(max_fitness, max(pop_fitness))
        count += 1


def evolutionary2(graph: Graph) -> list | str:
    """_summary_:
        Evolutionary algorithm main. Initialize a population then loops until
        a fit enough path is found after a certain number of generations, 
        or if the 1000th generation is reached.

    Args:
        graph (Graph): Graph structure where to look for the shortest path

    Returns:
        str | list: 
            On failure, returns 'failure'
            On success, returns the list containing the path
    """
    count = 0
    start_time = time.time()
    populations = 0
    generation = 10
    max_fitness = 0
    verticies = graph.get_verticies()
    permutations = list(it.permutations(verticies))
    population = rd.sample(permutations, 5)
    population = [list(indiv) for indiv in population]
    while True:
        if count > 1000:
            print(f'Elapsed time is 999999999999999999999999ms')
            print(f'Number of populations: 999999999999999999999999')
            return 'failure'
        populations += 1
        print(population)
        pop_fitness = list(fitness4(graph, population, len(verticies)))
        print(pop_fitness)
        if generation <= 0 and max(pop_fitness) >= max_fitness:
            end = time.time() - start_time
            print(f'Elapsed time is {end * 1000:.2f}ms')
            print(f'Number of populations: {populations}')
            return population[pop_fitness.index(max(pop_fitness))]
        population = selection2(population, pop_fitness,
                                verticies, permutations)
        generation -= 1
        max_fitness = max(max_fitness, max(pop_fitness))
        count += 1


def evolutionary(graph: Graph) -> list | str:
    """_summary_:
        Evolutionary algorithm main. Initialize a population then loops until
        a fit enough path is found, or if the 1000th generation is reached.

    Args:
        graph (Graph): Graph structure where to look for the shortest path

    Returns:
        str | list: 
            On failure, returns 'failure'
            On success, returns the list containing the path
    """
    count = 0
    start_time = time.time()
    populations = 0
    verticies = graph.get_verticies()
    population = rd.sample(list(it.permutations(verticies)), 5)
    population = [list(indiv) for indiv in population]
    while True:
        if count > 1000:
            print(f'Elapsed time is 999999999999999999999999ms')
            print(f'Number of populations: 999999999999999999999999')
            return 'failure'
        populations += 1
        print(population)
        pop_fitness = list(fitness4(graph, population, len(verticies)))
        print(pop_fitness)
        if max(pop_fitness) >= 70.0:
            end = time.time() - start_time
            print(f'Elapsed time is {end * 1000:.2f}ms')
            print(f'Number of populations: {populations}')
            return population[pop_fitness.index(max(pop_fitness))]
        population = selection(population, pop_fitness, verticies)
        count += 1
        # input()
