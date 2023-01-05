"""
Tests for solver.py
"""

import solver


def test_fetchWordList():
    """
    Test that word list is fetched correctly.
    """
    solverInstance = solver.WordleSolver()
    wordlist = solverInstance.master_wordlist
    assert ('women' in wordlist)
    assert ('abyss' in wordlist)
    assert ('death' in wordlist)


def test_autoSolver():
    """
    Test that the program can play against itself.
    """
    solverInstance = solver.WordleSolver()
    print(solverInstance.true_word)
    print(solverInstance.true_num_letters)

    success = False
    while success is False:
        guess = solverInstance.suggestGuess()
        print(guess)
        success = solverInstance.processGuess(guess)

    assert (success is True)


test_fetchWordList()
test_autoSolver()
