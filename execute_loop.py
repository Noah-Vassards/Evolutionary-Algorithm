import subprocess
from path_length import path_len

solutions = []
times = []
populations = []
times_per_generation = []
paths_len = []
failure = 0
success = 0

executions = 100

for _ in range(executions):
    # print('simulation ', i)
    proc = subprocess.Popen(
        ['./TSP.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # execute ./TSP.py and catch all outputs
    output = proc.communicate()[0].decode().split('\n')[:-1]
    # transform the output into a list containing each lines
    solution = output[-1]
    if solution != 'failure':
        solutions.append(solution)
        paths_len.append(path_len(eval(solution)))
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


print(*zip(solutions, times, populations, times_per_generation, paths_len), sep='\n')
print()
print('Average total time:', round(sum(times)/len(times), 2)
      if len(times) > 0 else 'NaN')
print('Average number of generation', int(sum(populations)/len(populations))
      if len(populations) > 0 else 'NaN')
print('Average time per generation:', round(sum(times_per_generation) /
      len(times_per_generation), 2) if len(times_per_generation) > 0 else 'NaN')
print(f'success rate:', (success * 100) / (failure + success))
print('Shortest path found:', (paths_len.count(194) * 100)/len(paths_len) if len(paths_len) > 0 else 'NaN')
