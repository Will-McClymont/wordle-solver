import userfunctions

print('Would you like suggestions? (Y/N)')
suggest = input()
if suggest.lower() == 'y':
    suggest = True
else:
    sugest = False

userfunctions.interactive_solve(suggest=suggest)
