import solver


def random_batch_solve(true_word, suppress_info=False):
    '''
    Function to solve for a given true word using the random method.
    '''

    solver_instance = solver.WordleSolver(true_word=true_word,
                                          suppress_info=suppress_info)

    success = False
    while not success:
        guess = solver_instance.suggest_random_guess()
        success = solver_instance.process_guess(guess)

    if guess == solver_instance.true_word:
        return guess, solver_instance.num_attempts
    else:
        raise ValueError('Unable to solve correctly...')


def eliminator_batch_solve(true_word, suppress_info=False):
    """
    Function to solve for a given true word using the eliminator method.
    """
    solver_instance = solver.WordleSolver(true_word=true_word,
                                          suppress_info=suppress_info)

    success = False
    while not success:
        guess = solver_instance.suggest_eliminator_guess(
            force_viable=True)
        success = solver_instance.process_guess(guess)

    if guess == solver_instance.true_word:
        return guess, solver_instance.num_attempts
    else:
        raise ValueError('Unable to solve correctly...')


def flagship_batch_solve(true_word, suppress_info=False):
    """
    Function to solve for a given true word using the eliminator method.
    """
    solver_instance = solver.WordleSolver(true_word=true_word,
                                          suppress_info=suppress_info)

    guess = solver_instance.suggest_default_first_guess()
    #guess = solver_instance.suggest_eliminator_guess()
    success = solver_instance.process_guess(guess)

    while not success:
        guess = solver_instance.suggest_eliminator_guess()
        success = solver_instance.process_guess(guess)

    if guess == solver_instance.true_word:
        return guess, solver_instance.num_attempts
    else:
        raise ValueError('Unable to solve correctly...')


def interactive_solve(true_word=None, suggest=True):
    """
    Function to allow the user to solve interactively.
    """
    solver_instance = solver.WordleSolver(true_word=true_word,
                                          suppress_info=False)

    if suggest:
        suggested_guess = solver_instance.suggest_default_first_guess()
        print(f'Suggested first guess: {suggested_guess}')

    success = False
    while not success:
        valid_guess = False
        if suggest:
            suggested_guess = solver_instance.suggest_eliminator_guess()
            print(f'Suggested  guess: {suggested_guess}')
        while not valid_guess:
            try:
                print('Please enter a valid guess.')
                guess = input()
                success = solver_instance.process_guess(guess)
                valid_guess = True
            except ValueError:
                print('Guess was not a valid five letter word that appears in'
                      'the Wordle dictionary.')

    if guess == solver_instance.true_word:
        return guess, solver_instance.num_attempts
    else:
        raise ValueError('Unable to solve correctly...')
