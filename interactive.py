'''
This script can be executed from the command line with Python3 in
order to play Wordle interactively.
'''

import userfunctions

print('Would you like suggestions? (Y/N)')
suggest = input()
if suggest.lower() == 'y':
    suggest = True
else:
    sugest = False

userfunctions.interactive_solve(suggest=suggest)
