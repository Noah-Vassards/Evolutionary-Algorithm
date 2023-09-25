import subprocess
from graph import Graph

solutions = []
times = []
populations = []
times_per_generation = []
failure = 0
success = 0

executions = 100

for _ in range(executions):
    proc = subprocess.Popen(
        ['./TSP.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # execute ./TSP.py and catch all outputs
    output = proc.communicate()[0].decode().split('\n')[:-1]
    # transform the output into a list containing each lines
    solution = output[-1]
    if solution != 'failure':
        solutions.append(solution)
        time = float(output[-3].split(' ')[-1].removesuffix('ms'))
        # gets only the time value
        times.append(time)
        population = int(output[-2].split(' ')[-1])
        # gets only the number of generated popultations
        populations.append(population)
        times_per_generation.append(round(time / population, 2))
        # compute the average time required to evaluate each generation
        success += 1
    else:
        failure += 1


print(*zip(solutions, times, populations, times_per_generation), sep='\n')
print()
print('mean total time:', round(sum(times)/len(times), 2)
      if len(times) > 0 else 'NaN')
print('mean popultation', int(sum(populations)/len(populations))
      if len(populations) > 0 else 'NaN')
print('mean time per generation', round(sum(times_per_generation) /
      len(times_per_generation), 2) if len(times_per_generation) > 0 else 'NaN')
print(f'success rate:', (success * 100) / (failure + success))
