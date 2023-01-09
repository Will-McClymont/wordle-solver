"""
Tests for userfunctions.py
"""

import userfunctions

words = ['women', 'death', 'abyss']
mixedcase_words = ['wOmen', 'DeatH', 'ABYSS']
spaceandcase_words = ['W O M E N', 'd e A tH', 'a b y s s']
fake_words = ['aaaaa', 'abcde', 'greip']
fake_spaceandcase_words = ['AAAAA', 'aBCdE', 'G re ip']


def test_random_batch_solve():
    """
    Test random batch solver works correctly.
    """
    # Normal inputs.
    for word in words:
        assert (userfunctions.random_batch_solve(word) == word)

    for word, test_word in zip(words, mixedcase_words):
        assert (userfunctions.random_batch_solve(test_word) == word)

    for word, test_word in zip(words, spaceandcase_words):
        assert (userfunctions.random_batch_solve(test_word) == word)

    for word in fake_words:
        assert (userfunctions.random_batch_solve(word) != word)

    for word in fake_spaceandcase_words:
        assert (userfunctions.random_batch_solve(word) != word)


def test_eliminator_batch_solve():
    """
    Test eliminator batch solver works correctly.
    """
    # Normal inputs.
    for word in words:
        assert (userfunctions.eliminator_batch_solve(word) == word)

    for word, test_word in zip(words, mixedcase_words):
        assert (userfunctions.eliminator_batch_solve(test_word) == word)

    for word, test_word in zip(words, spaceandcase_words):
        assert (userfunctions.eliminator_batch_solve(test_word) == word)

    for word in fake_words:
        assert (userfunctions.eliminator_batch_solve(word) != word)

    for word in fake_spaceandcase_words:
        assert (userfunctions.eliminator_batch_solve(word) != word)
