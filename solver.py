"""
This module is the core of the Wordle solver program. The
main feature is the WordleSolver class.
"""

import numpy as np
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


class WordleSolver():

    def __init__(self,
                 wordlist_path=r'all_words.txt',
                 true_word=None,
                 suppress_info=False
                 ):
        '''
        Initialise the solver. Set attributes to their default values,
        attempt to set the true_word and fetch the wordlist.

        Parameters
        ----------
        wordlist_path: str
            the path for the wordlist.
        true_word: str
            the input word to be set as the answer for the Wordle.
            must be a valid 5 letter word, otherwise a random word
            is set.
        suppress_info: boolean
            if set to true, will stop most information from being printed.
            can be useful if solving many words in batch.
        '''
        self.wordlist_path = wordlist_path
        self.fetch_word_list()
        self.viable_wordlist = self.master_wordlist[:]
        self.suppress_info = suppress_info

        self.num_attempts = 0
        self.known_letters = ['*', '*', '*', '*', '*']
        self.known_falseletters = [[], [], [], [], []]
        self.minnum_letters = np.zeros(26, dtype=int)
        self.maxnum_letters = np.ones(26, dtype=int) * 5

        self.set_true_word(true_word)

    def sanitise_word(self, word):
        '''
        Sanitises an input word by removing spaces and converting to lower
        case.
        Parameters
        ----------
        word: str
            the input word to be sanitised

        Returns
        ----------
        sanitised_word: str
            the sanitised word as a five letter lowercase string
        '''
        sanitised_word = word.replace(" ", "")
        sanitised_word = sanitised_word.lower()

        if len(sanitised_word) != 5:
            raise ValueError(
                f'Unable to convert {word} to a five letter lowercase word.')

        if sanitised_word not in self.master_wordlist:
            raise ValueError(
                f'Input word \'{word}\' is not in the Wordle dictionary.')

        return sanitised_word

    def output_word(self, word):
        '''
        Converts an all lower case word to all caps and includes codes to
        show as coloured text when printed.

        Parameters
        ----------
        word: str
            the input word to be converted to output format.

        Returns
        ----------
        output_string: str
            the word in output format, suitable to be sent to print
            in colour.
        '''

        word = self.sanitise_word(word)

        output_string = ""

        running_num_letters = np.zeros(26, dtype=int)
        for i, letter in enumerate(word):
            index = ord(letter) - ord('a')
            if letter == self.true_word[i]:
                output_string = (f'{output_string}{Fore.CYAN}'
                                 f'{letter.upper()}{Style.RESET_ALL}')
                continue
            elif self.true_num_letters[index] > running_num_letters[index]:
                running_num_letters[index] += 1
                output_string = (f'{output_string}{Fore.YELLOW}'
                                 f'{letter.upper()}{Style.RESET_ALL}')
                continue
            elif self.true_num_letters[index] == running_num_letters[index]:
                output_string = (f'{output_string}{Fore.RED}'
                                 f'{letter.upper()}{Style.RESET_ALL}')
                continue

        return output_string

    def set_true_word(self, true_word):
        '''
        Sets the true_word attribute to the true_word provided.
        Sets to a random word on the master list if true_word is None or
        invalid.

        Parameters
        ----------
        word: str
            the input word to be set as the answer for the Wordle.
            must be a valid 5 letter word, otherwise a random word
            is set.
        '''

        if true_word is None:
            number_of_words = len(self.master_wordlist)
            random_index = np.random.randint(number_of_words)
            self.true_word = self.master_wordlist[random_index]

        else:
            try:
                self.true_word = self.sanitise_word(true_word)
            except ValueError:
                if not self.suppress_info:
                    print('Input true word not valid. '
                          'Setting random true word.')
                number_of_words = len(self.master_wordlist)
                random_index = np.random.randint(number_of_words)
                self.true_word = self.master_wordlist[random_index]

        self.true_num_letters = np.zeros(26, dtype=int)
        for i, letter in enumerate(self.true_word):
            self.true_num_letters[ord(letter) - ord('a')] += 1

    def fetch_word_list(self):
        '''
        Fetches the master word list from the specificed file and returns the
        words as a list.
        '''
        with open(self.wordlist_path, 'r') as file:
            self.master_wordlist = [line.rstrip() for line in file]

        num_words = len(self.master_wordlist)
        self.master_wordlist_num_letters = np.zeros((num_words, 26),
                                                    dtype=int)
        for i, word in enumerate(self.master_wordlist):
            for letter in word:
                self.master_wordlist_num_letters[i, ord(
                    letter) - ord('a')] += 1

        self.wordlist_num_letters = np.copy(self.master_wordlist_num_letters)

    def process_guess(self, guess):
        '''
        Takes an input guess, checks its validity, and updates the class
        attributes with new information from that guess, e.g. removing
        nonviable words from the viable_words list.

        Parameters
        ----------
        guess: str
            the input word to be processed as a guess.
            must be a valid five letter word.

        Returns
        ----------
        boolean
            whether or not the guess is correct
        '''

        # Check that the guess is a valid word
        try:
            guess = self.sanitise_word(guess)
        except ValueError:
            raise ValueError(
                f'{guess} is not a valid 5 letter word. Guess not processed.')

        self.num_attempts += 1

        if not self.suppress_info:
            print(self.output_word(guess))

        # Check if the guess is correct
        if guess == self.true_word:
            if not self.suppress_info:
                print(
                    f'You have successfully guessed the word after '
                    f'{self.num_attempts} attempts!')
            return True

        guess_num_letters = np.zeros(26, dtype=int)
        # Update the lists with new knowledge from guess
        for i, letter in enumerate(guess):
            guess_num_letters[ord(letter) - ord('a')] += 1
            if letter is self.true_word[i]:
                self.known_letters[i] = letter
            else:
                self.known_falseletters[i].append(letter)

        too_many_mask = guess_num_letters > self.true_num_letters
        exact_mask = guess_num_letters == self.true_num_letters
        too_few_mask = guess_num_letters < self.true_num_letters

        # When you guess too many of a letter, you know the exact number of
        # that letter in the true word.

        self.minnum_letters = np.where(too_many_mask,
                                       self.true_num_letters,
                                       self.minnum_letters)

        self.maxnum_letters = np.where(too_many_mask,
                                       self.true_num_letters,
                                       self.maxnum_letters)

        # When you guess the correct number or too few of a letter,
        # you have updated knowledge about the minimum number of that letter,
        # but only if your new knowledge
        # is more restrictive than the previous knowledge gained.

        self.minnum_letters = np.where(too_few_mask | exact_mask,
                                       np.maximum(guess_num_letters,
                                                  self.minnum_letters),
                                       self.minnum_letters)

        self.eliminate_nonviable_words()

        return False

    def eliminate_nonviable_words(self):
        '''
        Eliminates words which are no longer valid given the restrictions from
        the current knowledge. The current knowledge is stored in the
        minnum_letter, maxnumletters, known_letters, and known_falseletters
        attributes.
        '''

        for i, word in enumerate(list(self.viable_wordlist)):
            # Check that the word doesn't violate known letter numbers
            if (np.any(self.wordlist_num_letters[i, :] < self.minnum_letters)
                    or np.any(self.wordlist_num_letters[i, :]
                              > self.maxnum_letters)):
                self.viable_wordlist.remove(word)
                continue

            for j, letter in enumerate(word):

                # Check that the word contains the true letter, if known
                if (self.known_letters[j] != '*'
                        and self.known_letters[j] != letter):
                    self.viable_wordlist.remove(word)
                    break

                # Otherwise, check that the letter isn't known to be false
                elif any(letter in x for x in self.known_falseletters[j][:]):
                    self.viable_wordlist.remove(word)
                    break

        self.wordlist_num_letters = np.zeros((len(self.viable_wordlist), 26),
                                             dtype=int)
        for i, word in enumerate(self.viable_wordlist):
            for letter in word:
                self.wordlist_num_letters[i, ord(letter) - ord('a')] += 1

    def suggest_random_guess(self):
        '''
        Suggests a random word from the viable_wordlist attribute.
        '''
        number_of_words = len(self.viable_wordlist)
        random_index = np.random.randint(number_of_words)
        return self.viable_wordlist[random_index]

    def suggest_eliminator_guess(self, force_viable=False):
        '''
        Suggest a guess to eliminate as many common letters as possible.

        parameters:
        force_viable: boolean
            Set to true in order to only select words that may still
            be the correct word.
        '''

        # Score number of words in which each letter appears

        wordlist_binary_letters = np.where(self.wordlist_num_letters > 0, 1, 0)
        letter_freq_list = np.sum(wordlist_binary_letters, axis=0, dtype=float)
        letter_freq_list *= 0.01 ** self.minnum_letters

        letter_freq_list = np.where(self.minnum_letters == self.maxnum_letters,
                                    0, letter_freq_list)

        # Score the wordlist by multiplying each of its letters by their
        # frequency. Double letters are only counted once.
        master_wordlist_binary_letters = np.where(
            self.master_wordlist_num_letters > 0, 1, 0)

        wordlist_scores = np.sum(
            wordlist_binary_letters * letter_freq_list, axis=1)
        highest_scoring_index = np.argmax(wordlist_scores)
        highest_scoring = wordlist_scores[highest_scoring_index]

        master_wordlist_scores = np.sum(
            master_wordlist_binary_letters * letter_freq_list, axis=1)
        highest_scoring_master_index = np.argmax(master_wordlist_scores)
        highest_scoring_master = \
            master_wordlist_scores[highest_scoring_master_index]

        if force_viable:
            return self.viable_wordlist[highest_scoring_index]
        elif not force_viable:
            if highest_scoring >= 0.99999 * highest_scoring_master:
                return self.viable_wordlist[highest_scoring_index]
            return self.master_wordlist[highest_scoring_master_index]

    def suggest_default_first_guess(self):
        '''
        Suggest a default first guess. This is a word that is known to
        be good at eliminating many possibilities, and likley better than
        the guess suggested by suggest_eliminator_guess.
        '''
        return 'salet'
