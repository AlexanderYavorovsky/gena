import random
import copy

template_config = {
    '--seed': range(1, 100),
    '--max-funcs': range(1, 600),
    '--max-expr-complexity': range(2, 500)
}

def generate_config():
    config = dict()
    for flag in template_config.keys():
        config[flag] = random.choice(template_config[flag])
    return config

def crossover_func(chrom1, chrom2):
    child1 = copy.deepcopy(chrom1)
    child2 = copy.deepcopy(chrom2)
    random_key = random.choice(list(chrom1.keys()))
    child1[random_key], child2[random_key] = child2[random_key], child1[random_key]
    return child1, child2

def mutation_func(chromosome):
    child = chromosome.copy()
    random_key = random.choice(list(chromosome.keys()))
    child[random_key] = random.choice(template_config[random_key])
    return child

def fitness_func(chromosome):
    result = sum(chromosome.values())
    if result != desired_output:
        fitness = 1.0 / abs(result - desired_output)
    else:
        fitness = 1
    return fitness

def population_sort(population, amount):
    sorted_list = sorted(population, key=lambda x: x[1], reverse=True)
    return sorted_list[:amount]

def mutation(population, amount):
    random_chromosomes = random.sample(population, amount)
    for element in random_chromosomes:
        result = mutation_func(element[0])
        population.append((result, 0))

def crossover(population, amount):
    random_chromosomes = random.sample(population, amount)
    for element in random_chromosomes:
        element2 = random.choice(random_chromosomes)
        child1, child2 = crossover_func(element[0], element2[0])
        population.append((child1, 0))
        population.append((child2, 0))


desired_output = 541
initial_population = []
for _ in range(10): 
    chromosome = generate_config()
    initial_population.append((chromosome, 0))

def genetic_func(population, iterations):
    
    for index, item in enumerate(population):
        result = fitness_func(item[0])
        population[index] = (item[0], result)
    
    for i in range(iterations):
        population = population_sort(population, 5)
        if population[0][1] == 1:
            print(i+1)
            break
        crossover(population, 3)
        mutation(population, 5)
        for index, item in enumerate (population[-5:]):
            result = fitness_func(item[0])
            population[-5 + index] = (item[0], result)
    return population   

best = genetic_func(initial_population, 10000)
print(best)