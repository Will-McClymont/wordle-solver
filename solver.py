"""
Main solver module.
"""

import numpy as np


def fetchWordList(path=r'all_words.txt'):

    with open(path, 'r') as file:
        words = [line.rstrip() for line in file]

    return words
