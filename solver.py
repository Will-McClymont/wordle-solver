"""
Main solver module.
"""

import numpy as np


class WordleSolver():

    def __init__(self,
                 wordlist_path=r'all_words.txt',
                 true_word=None
                 ):
        self.wordlist_path = wordlist_path
        self.fetch_word_list()
        self.viable_wordlist = self.master_wordlist[:]

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
        '''
        sanitised_word = word.replace(" ", "")
        sanitised_word = sanitised_word.lower()

        if len(sanitised_word) != 5:
            raise ValueError(f'Unable to convert {word} to a five letter lowercase word.')

        if sanitised_word not in self.master_wordlist:
            raise ValueError(f'Input word \'{word}\' is not in the Wordle dictionary.')

        return sanitised_word

    def output_word(self, word):
        '''
        Converts an all lower case word to all caps and provides a list of
        values corresponding to the letter colour.
        '''

    def set_true_word(self, true_word):
        '''
        Sets the true_word attribute to the true_word provided.
        Sets to a random word on the master list if true_word is None or
        invalid.
        '''

        if true_word is None:
            number_of_words = len(self.master_wordlist)
            random_index = np.random.randint(number_of_words)
            self.true_word = self.master_wordlist[random_index]

        elif true_word in self.master_wordlist:
            self.true_word = true_word

        else:
            print('Input true word not valid. Setting random master word.')
            number_of_words = len(self.master_wordlist)
            random_index = np.random.randit(number_of_words)
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

        self.master_wordlist_num_letters = np.zeros((len(self.master_wordlist), 26),
                                                    dtype=int)
        for i, word in enumerate(self.master_wordlist):
            for letter in word:
                self.master_wordlist_num_letters[i, ord(
                    letter) - ord('a')] += 1

        self.wordlist_num_letters = np.copy(self.master_wordlist_num_letters)

    def process_guess(self, guess):

        # Check that the guess is a valid word
        if guess not in self.master_wordlist:
            print('Guess was not a valid 5 letter word. Guess not processed.')
            return False
        else:
            self.num_attempts += 1

        # Check if the guess is correct
        if guess is self.true_word:
            print(
                f'You have successfully guessed the word after {self.num_attempts} attempts!')
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

        print(self.minnum_letters)
        print(self.maxnum_letters)
        self.eliminate_nonviable_words()

        return False

    def eliminate_nonviable_words(self):

        for i, word in enumerate(list(self.viable_wordlist)):
            # Check that the word doesn't violate known letter numbers
            # THIS NEEDS TO BE DFIXED TO USE VIABLEWORDLIST_NUM_LETTERS
            if np.any(self.wordlist_num_letters[i, :] < self.minnum_letters) or np.any(self.wordlist_num_letters[i, :] > self.maxnum_letters):
                self.viable_wordlist.remove(word)
                continue

            for j, letter in enumerate(word):

                # Check that the word contains the true letter, if known
                if self.known_letters[j] != '*' and self.known_letters[j] != letter:
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
        number_of_words = len(self.viable_wordlist)
        random_index = np.random.randint(number_of_words)
        return self.viable_wordlist[random_index]

    def suggest_eliminator_guess(self, force_viable=False):
        '''
        Suggest a guess to eliminate as many common letters as possible.

        parameters:
        force_viable - Set to true in order to only select words that may still
                       be the correct word.
        '''

        # Score number of words in which each letter appears

        wordlist_binary_letters = np.where(self.wordlist_num_letters > 0, 1, 0)
        letter_freq_list = np.sum(wordlist_binary_letters, axis=0)
        letter_freq_list = np.where(
            self.minnum_letters > 0, 0, letter_freq_list)
        letter_freq_list = np.where(
            self.maxnum_letters == 0, 0, letter_freq_list)
        letter_freq_list = np.where(
            self.maxnum_letters == self.minnum_letters, 0, letter_freq_list)

        # Score the wordlist by multiplying each of its letters by their
        # frequency. Double letters are only counted once.
        if not force_viable:
            wordlist_binary_letters = np.where(
                self.master_wordlist_num_letters > 0, 1, 0)

        wordlist_scores = np.sum(
            wordlist_binary_letters * letter_freq_list, axis=1)
        highest_scoring_index = np.argmax(wordlist_scores)
        print(np.shape(wordlist_scores))
        print(highest_scoring_index)
        print(len(self.viable_wordlist))

        if force_viable:
            return self.viable_wordlist[highest_scoring_index]
        elif not force_viable:
            return self.master_wordlist[highest_scoring_index]

    def suggest_default_first_guess(self):
        return 'shoal'

    def suggest_smart_guess(self):
        '''
        Suggest a guess from the list of viable remaining words based on a
        criteria for which word is most likley.
        '''
