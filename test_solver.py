"""
Tests for solver.py
"""

import solver
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

words = ['women', 'death', 'abyss']
mixedcase_words = ['wOmen', 'DeatH', 'ABYSS']
spaceandcase_words = ['W O M E N', 'd e A tH', 'a b y s s']
fake_words = ['aaaaa', 'abcde', 'greip']
fake_spaceandcase_words = ['AAAAA', 'aBCdE', 'G re ip']


def test_fetch_wordlist():
    """
    Test that word list is fetched correctly.
    """
    solver_instance = solver.WordleSolver()
    wordlist = solver_instance.master_wordlist

    for word in words:
        assert (word in wordlist)

    for word in fake_words:
        assert (word not in wordlist)


def test_sanitise_word():
    """
    Test that words are correctly converted to 5 letter lowercase
    or are rejected.
    """
    solver_instance = solver.WordleSolver()

    for word in words:
        assert (solver_instance.sanitise_word(word) == word)

    for word, test_word in zip(words, mixedcase_words):
        assert (solver_instance.sanitise_word(test_word) == word)

    for word, test_word in zip(words, spaceandcase_words):
        assert (solver_instance.sanitise_word(test_word) == word)

    for word in fake_words:
        try:
            solver_instance.sanitise_word(word)
            raise AssertionError
        except ValueError:
            pass

    for word in fake_spaceandcase_words:
        try:
            solver_instance.sanitise_word(word)
            raise AssertionError
        except ValueError:
            pass


def test_output_word():
    '''
    Test that the logic for highlighting letters works correctly.
    '''
    solver_instance = solver.WordleSolver()
    solver_instance.set_true_word('shoal')
    output = solver_instance.output_word('books')
    desired_output = (f'{Fore.RED}B{Style.RESET_ALL}'
                      f'{Fore.RED}O{Style.RESET_ALL}'
                      f'{Fore.CYAN}O{Style.RESET_ALL}'
                      f'{Fore.RED}K{Style.RESET_ALL}'
                      f'{Fore.YELLOW}S{Style.RESET_ALL}')
    assert(output == desired_output)


def test_set_true_word():
    """
    Test that the true word is only set to valid inputs.
    """
    solver_instance = solver.WordleSolver()

    for word in words:
        solver_instance = solver.WordleSolver()
        solver_instance.set_true_word(word)
        assert (solver_instance.true_word == word)

    for word, test_word in zip(words, mixedcase_words):
        solver_instance = solver.WordleSolver()
        solver_instance.set_true_word(test_word)
        assert (solver_instance.true_word == word)

    for word, test_word in zip(words, spaceandcase_words):
        solver_instance = solver.WordleSolver()
        solver_instance.set_true_word(test_word)
        assert (solver_instance.true_word == word)

    for word in fake_words:
        solver_instance = solver.WordleSolver()
        solver_instance.set_true_word(word)
        assert (solver_instance.true_word != word)

    for word in fake_spaceandcase_words:
        solver_instance = solver.WordleSolver()
        solver_instance.set_true_word(word)
        assert (solver_instance.true_word != word)


def test_process_guess():
    """
    Test that only words in the wordle list are able to be used as guesses
    and that they are removed from the viable wordlist.

    This also tests the eliminate_nonviable_words method.
    """

    for word in words:
        solver_instance = solver.WordleSolver()
        solver_instance.process_guess(word)
        assert (word not in solver_instance.viable_wordlist)

    for word, test_word in zip(words, mixedcase_words):
        solver_instance = solver.WordleSolver()
        solver_instance.process_guess(test_word)
        assert (word not in solver_instance.viable_wordlist)

    for word, test_word in zip(words, spaceandcase_words):
        solver_instance = solver.WordleSolver()
        solver_instance.process_guess(test_word)
        assert (word not in solver_instance.viable_wordlist)

    for word in fake_words:
        try:
            solver_instance = solver.WordleSolver()
            solver_instance.process_guess(word)
            raise AssertionError
        except ValueError:
            pass

    for word in fake_spaceandcase_words:
        try:
            solver_instance = solver.WordleSolver()
            solver_instance.process_guess(word)
            raise AssertionError
        except ValueError:
            pass


def test_suggest_random_guess():
    '''
    Test that suggest random words are valid and viable.
    '''

    solver_instance = solver.WordleSolver(true_word='green')

    # Check that the random words are in the master list
    for i in range(10000):
        guess = solver_instance.suggest_random_guess()
        assert(guess in solver_instance.master_wordlist)

    # Check that the random words are viable after some have been
    # eliminated from a guess
    solver_instance.process_guess('grape')
    for i in range(10000):
        guess = solver_instance.suggest_random_guess()
        assert(guess in solver_instance.viable_wordlist)


def test_suggest_eliminator_guess():
    '''
    Test that suggested guesses are valid and viable.
    '''

    solver_instance = solver.WordleSolver(true_word='green')

    # Check that the suggested guesses are in the master list
    for i in range(10000):
        guess = solver_instance.suggest_eliminator_guess()
        assert(guess in solver_instance.master_wordlist)

    # Check that the suggested guesses are viable after some have been
    # eliminated from a guess, but only if force_viable is set
    solver_instance.process_guess('grape')
    guess = solver_instance.suggest_eliminator_guess(force_viable=True)
    assert(guess in solver_instance.viable_wordlist)


def test_suggest_default_first_guess():
    '''
    Check that the default suggested guess is valid and viable.
    '''
    solver_instance = solver.WordleSolver()
    guess = solver_instance.suggest_default_first_guess()
    assert(guess == solver_instance.sanitise_word(guess))
