# wordle-solver

## Description

This program was designed to help you solve Wordle. It can be run in an interactive mode with or without suggestions, or it can be run in a batch mode to see how well it would do. It follows a simple algorithm to try and eliminate as many letters as possible before suggesting words which are likley to be correct.

## Installation

The contents of this repository can be retrived using git and the code can be run as long as Python 3(.10) is installed with the packages listed in requirements.txt.

Alternatively, the Dockerfile contained in this repository can be built and run using Docker to create an Ubuntu virtual machine. Move the Dockerfile to a new directory and change to that directory, then run these commands:

'''
docker build -t wordlesolver
docker run --rm --ti wordlesolver
'''

You can then move to the wordle-solver directory in the virtual machine and follow the instructions to run the code. 

## How to Run

The userfunctions.py module can be imported into any Python script where you want to include a Wordle solver, such as in a larger games library.

Alternatively, wordle-solver can be played in an interactive mode from the command line using:
'''
python3 interactive.py
'''
You will be asked whether you want to be given suggested guesses, which can be confimed by entering 'Y' or 'N' into the terminal. You can then enter guesses until you guess the correct word.

If you want to test how well wordle-solver can handle a particular word, you can use the batch.py script with:
'''
python3 batch.py word suppress
'''
Replace 'word' with the five letter word that you want to test. It must appear in the all_words.txt file, which is the Wordle dictionary by default. The 'suppress' argument should be either 'Y' or 'N' to indicate whether you would like wordle-solver to supress most of its output. This can be useful if you are testing many words. If no suppress argument is given, 'Y' is assumed.

The efficency.py script is also included, which generates a bar chart of the number of guesses required to guess each word on the wordlist. 


## Credits

Written by William McClymont.