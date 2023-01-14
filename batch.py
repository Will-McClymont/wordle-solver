'''
This script can be executed from the command line with Python3 in
order to batch solve Wordle for a given word or a randomly assigned
word.

    >>> python3 batch.py word suppress

Replace 'word' with the five letter word that you want to test.
It must appear in the all_words.txt file, which is the Wordle
dictionary by default. The 'suppress' argument should be either
'Y' or 'N' to indicate whether you would like wordle-solver to
supress most of its output. This can be useful if you are testing
many words. If no suppress argument is given, 'Y' is assumed.
'''

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
