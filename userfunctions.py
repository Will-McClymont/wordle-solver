'''
This module contains functions that are used in the interactive.py
and batch.py scripts. These functions are also suitable for a user
to incorporate into their own scripts. The functions handle the
interation with the WordleSolver class from the solver module.

Contains:
----------------------------------------
    random_batch_solve
        Solves Wordle for a given true word by guessing random viable
        words.
    eliminator_batch_solve
        Solves Wordle for a given true word by guessing words which will
        eliminate many remaining viable words.
    flagship_batch_solve
        Solves Wordle for a given true word by guessing mainly using the
        eliminator method, however some tweaks are used to improve
        performance.
    interactive_solve
        This function is used to play Wordle interactively.
'''

import solver


def random_batch_solve(true_word, suppress_info=False):
    '''
    Function to solve for a given true word using the random method.

    Parameters
    ----------
    true_word: str
        the input word to be set as the answer for the Wordle.
        must be a valid 5 letter word, otherwise a random word
        is set.
    suppress_info: boolean
        if set to true, will stop most information from being printed.
        can be useful if solving many words in batch.

    Returns
    ----------
    str
        the actual true word used by the Wordle solver. Can be useful
        in can a random true word was set due to an invalid input.
    int
        the number of attempts taken to solve the Wordle.
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
    '''
    Function to solve for a given true word using the eliminator method.

    Parameters
    ----------
    true_word: str
        the input word to be set as the answer for the Wordle.
        must be a valid 5 letter word, otherwise a random word
        is set.
    suppress_info: boolean
        if set to true, will stop most information from being printed.
        can be useful if solving many words in batch.

    Returns
    ----------
    str
        the actual true word used by the Wordle solver. Can be useful
        in can a random true word was set due to an invalid input.
    int
        the number of attempts taken to solve the Wordle.
    '''
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
    '''
    Function to solve for a given true word using the best method.

    Parameters
    ----------
    true_word: str
        the input word to be set as the answer for the Wordle.
        must be a valid 5 letter word, otherwise a random word
        is set.
    suppress_info: boolean
        if set to true, will stop most information from being printed.
        can be useful if solving many words in batch.

    Returns
    ----------
    str
        the actual true word used by the Wordle solver. Can be useful
        in can a random true word was set due to an invalid input.
    int
        the number of attempts taken to solve the Wordle.
    '''
    solver_instance = solver.WordleSolver(true_word=true_word,
                                          suppress_info=suppress_info)

    guess = solver_instance.suggest_default_first_guess()
    success = solver_instance.process_guess(guess)

    while not success:
        if len(solver_instance.viable_wordlist) <= 3:
            guess = solver_instance.suggest_eliminator_guess(force_viable=True)
        else:
            guess = solver_instance.suggest_eliminator_guess()
        success = solver_instance.process_guess(guess)

    if guess == solver_instance.true_word:
        return guess, solver_instance.num_attempts
    else:
        raise ValueError('Unable to solve correctly...')


def interactive_solve(true_word=None, suggest=True):
    '''
    Function to allow the user to solve interactively.

    Parameters
    ----------
    true_word: str
        the input word to be set as the answer for the Wordle.
        must be a valid 5 letter word, otherwise a random word
        is set.
    suppress_info: boolean
        if set to true, will stop most information from being printed.
        can be useful if solving many words in batch.

    Returns
    ----------
    str
        the actual true word used by the Wordle solver. Can be useful
        in can a random true word was set due to an invalid input.
    int
        the number of attempts taken to solve the Wordle.
    '''
    solver_instance = solver.WordleSolver(true_word=true_word,
                                          suppress_info=False)

    if suggest:
        suggested_guess = solver_instance.suggest_default_first_guess()
        print(f'Suggested first guess: {suggested_guess}')

    success = False
    while not success:
        valid_guess = False
        while not valid_guess:
            try:
                print('Please enter a valid guess.')
                guess = input()
                success = solver_instance.process_guess(guess)
                valid_guess = True
            except ValueError:
                print('Guess was not a valid five letter word that appears in'
                      'the Wordle dictionary.')
        if suggest and not success:
            suggested_guess = solver_instance.suggest_eliminator_guess()
            print(f'Suggested  guess: {suggested_guess}')

    if guess == solver_instance.true_word:
        return guess, solver_instance.num_attempts
    else:
        raise ValueError('Unable to solve correctly...')
