'''
This script can be executed from the command line with Python3 in
order to play Wordle interactively.

    >>> python3 interactive.py
'''

import userfunctions

print('wordle-solver  Copyright (C) 2023 William McClymont')
print('This program comes with ABSOLUTELY NO WARRANTY.')
print('This is free software, and you are welcome to redistribute it')
print('under certain conditions. See licence.txt for details.')
print(' ')
print('--------------------------------------------------------------')
print(' ')
print('Welcome to the interactive wordle-solver.')
print(' ')
print('Would you like suggestions? (Y/N)')
suggest = input()
if suggest.lower() == 'y':
    suggest = True
else:
    suggest = False

userfunctions.interactive_solve(suggest=suggest)
