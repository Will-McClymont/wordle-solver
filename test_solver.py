"""
Tests for solver.py
"""

import solver


def test_fetchWordList():
    """
    Test that word list is fetched correctly.
    """
    wordlist = solver.fetchWordList()
    assert ('women' in wordlist)
    assert ('abyss' in wordlist)
    assert ('death' in wordlist)
