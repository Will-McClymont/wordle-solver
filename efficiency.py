import solver
import userfunctions

import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

solver_instance = solver.WordleSolver()

step = 20
wordlist = solver_instance.master_wordlist[::step]

method_name = 'Flagship'
#method_name = 'Random'
#method_name = 'Eliminator'
num_attempts = np.zeros(len(wordlist), dtype=int)

for i, word in enumerate(tqdm(wordlist)):
    if method_name == 'Flagship':
        word, attempts = userfunctions.flagship_batch_solve(word, True)
    elif method_name == 'Random':
        word, attempts = userfunctions.random_batch_solve(word, True)
    elif method_name == 'Eliminator':
        word, attempts = userfunctions.eliminator_batch_solve(word, True)
    num_attempts[i] = int(attempts)

avg = np.mean(num_attempts)
std = np.std(num_attempts)
med = np.median(num_attempts)
print(f'{method_name} Attempt Summary')
print(f'AVG: {round(avg, 2)}')
print(f'STD: {round(std, 2)}')
print(f'MED: {round(med, 2)}')

values, counts = np.unique(num_attempts, return_counts=True)

plt.bar(values, counts, color='black',
        label=f'{method_name}')
plt.axvline(avg, color='cyan', linewidth=2,
            label=f'AVG: {round(avg, 2)}'r'$\pm$'f'{round(std, 2)}')
plt.axvline(med, color='red', linewidth=2,
            label=f'MED: {round(med, 2)}')
plt.xlabel('Number of Attempts')
plt.ylabel("Number of Words")
# plt.title(f'{method_name}')
plt.grid()
plt.legend()
plt.savefig(f'{method_name}_hist.png')
plt.close()
