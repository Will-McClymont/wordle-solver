import userfunctions
import sys

true_word = sys.argv[1]

try:
    suppress_info = sys.argv[2]
    if suppress_info.lower() == 'n':
        suppress_info = False
    else:
        suppress_info = True
except IndexError:
    suppress_info = True

final_guess, num_attempts = \
    userfunctions.flagship_batch_solve(true_word=true_word,
                                       suppress_info=suppress_info)

print(f'Word: {final_guess}')
print(f'Number of Attempts: {num_attempts}')
