import random
import copy
import subprocess
import os
import argparse
from pathlib import Path

csmith_dir = 'csmith'
gen_dir = 'generated'
out_dir = Path(__file__).resolve().parent / gen_dir
gem5_dir = Path.cwd().parent / 'gem5'
gen_filename = 'my1.c'
out_filename = 'my1.out'



template_config = {
    '--seed': range(1, 100),
    '--max-funcs': range(1, 10),
    '--max-expr-complexity': range(2, 50)
}

def generate_config():
    config = dict()
    for flag in template_config.keys():
        config[flag] = str(random.choice(template_config[flag]))
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
    child[random_key] = str(random.choice(template_config[random_key]))
    return child

def fitness_func(chromosome):
    generate(gen_filename, chromosome)
    build(gen_filename, out_filename)
    print(f'Generated file {os.path.join(gen_dir, gen_filename)}'
      f' and built it into {os.path.join(gen_dir, out_filename)}')
    
    subprocess.run(['cp', out_dir / out_filename, gem5_dir / out_filename])
    os.chdir(gem5_dir)
    subprocess.run([gem5_dir / 'build/RISCV/gem5.opt', 'simple.py'])

    result = random.randint(1, 100)
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


desired_output = 10
initial_population = []
for _ in range(10): 
    chromosome = generate_config()
    initial_population.append((chromosome, 0))
    

def generate(dest_name, config):
    if not out_dir.is_dir():
        out_dir.mkdir(parents=True)
    os.chdir(out_dir)

    # TODO: arguments from mutation
    run_process = ['/usr/local/bin/csmith']
    for flag in config.keys():
        run_process.append(flag)
        run_process.append(config[flag])
    gen_proc = subprocess.run(run_process, capture_output=True, text=True)

    with open(dest_name, 'w') as f:
        f.write(gen_proc.stdout)

def build(src_name, dest_name):
    # TODO: use unknown elf instead
    subprocess.run(
        ['riscv64-linux-gnu-gcc', '--static', '-O0',
         '-I/usr/local/include', src_name, '-o', dest_name],
        capture_output=True)
    os.chdir('..')

def genetic_func(population, iterations):
    subprocess.run(['cp', 'simple.py', gem5_dir / 'simple.py'])
    
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

best = genetic_func(initial_population, 10)
print(best)