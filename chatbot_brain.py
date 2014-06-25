import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

from trainbot import Trainbot
import input_filters


class Chatbot(Trainbot):

    def __init__(self, training_file="tell_tale_heart.txt"):
        super(Chatbot, self).__init__(training_file="tell_tale_heart.txt")
        self.training_file = training_file

    def i_filter_random(self, words, lexicon=None):
        u"""Return randomly selected, non-punctuation word from words."""
        count = 0
        while count < len(words):
            seed = random.choice(words)
            if (seed in self.bi_lexicon) and (seed not in self.stop_puncts):
                return seed
            count += 1
        return "What a funny thing to say!"

    def o_filter_random(self, sentences):
        u"""Return randomly selected sentence from sentecnces"""
        return random.choice(sentences)

    def _create_chains(self, pair, size=1):
        u"""Return list of markov generated strings spawned from the seed."""
        candidates = []
        # import pdb
        # pdb.set_trace()
        # while len(candidates) < size:
        word_1 = pair[0]
        word_2 = pair[1]
        candidate = [word_1, word_2]
        pair = "{} {}".format(word_1, word_2)
        done = False
        while not done:
            try:
                next_word = random.choice(self.tri_lexicon[pair])
                candidate.append(next_word)
                print candidate
                word_1, word_2 = word_2, next_word
                pair = "{} {}".format(word_1, word_2)
            except KeyError:
                candidate.append(next_word)
                candidates.append(" ".join(candidate))
                done = True
            if next_word in self.stop_puncts:
                candidate.append(next_word)
                candidates.append(" ".join(candidate))
                done = True
        return candidates

    def _pair_seed(self, seed):
        word_1 = seed
        word_2 = None
        while word_2 is None:
            try:
                word_2 = random.choice(self.bi_lexicon[seed])
                pair = [word_1, word_2]
            except KeyError:
                continue
        return pair

    def compose_response(self, input_sent, input_filter=None, output_filter=None, lexicon=None):
        u"""Return a response sentence based on the input."""
        # Tokenize input
        seeds = wordpunct_tokenize(input_sent)
        # Select seed based on input filter
        if input_filter:
            seeds = input_filter(seeds, lexicon)
            #If a default sentence was picked, return it.
            if isinstance(seeds, basestring):
                return seeds
        # Randomly pick a seed from the returned possibilities.
        seed = self.i_filter_random(seeds)
        # Create chains
<<<<<<< HEAD
        chains = self._create_chains(seed)
=======
        pair = self._pair_seed(seed)
        chains = self._create_chains(pair)
>>>>>>> 69d0a2fc0558ffa5c6950de0700b45d431b6aca1
        # Return output of filter
        # return output_filter(chains)
        return chains

if __name__ == '__main__':
    bot = Chatbot()
    bot.fill_lexicon()
    print "Filled the lexicon!"
    print bot.compose_response("My beautiful carriage is red and blue and it hums while I drive it!",
        input_filters.filter_content_priority, bot.o_filter_random, bot.bi_lexicon)


