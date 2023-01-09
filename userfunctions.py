import solver


def random_batch_solve(true_word):
    '''
    Function to solve for a given true word using the random method.
    '''

    solver_instance = solver.WordleSolver(true_word=true_word)

    success = False
    while success is False:
        guess = solver_instance.suggest_random_guess()
        print(guess)
        success = solver_instance.process_guess(guess)

    if guess == solver_instance.true_word:
        return guess
    else:
        raise ValueError('Unable to solve correctly...')


def eliminator_batch_solve(true_word):
    """
    Function to solve for a given true word using the eliminator method.
    """
    solver_instance = solver.WordleSolver(true_word=true_word)

    success = False
    while success is False:
        guess = solver_instance.suggest_eliminator_guess(
            force_viable=True)
        print(guess)
        success = solver_instance.process_guess(guess)

    if guess == solver_instance.true_word:
        return guess
    else:
        raise ValueError('Unable to solve correctly...')
