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
        return str(random.choice(sentences))

    def _create_chains(self, seed, size=10):
        u"""Return list of markov generated strings spawned from the seed."""
        response_candidates = []
        while len(response_candidates) < size:
            bad_sentence = False
            candidate_sentence = [seed]
            while True:
                word_2 = None
                next_word = None
                while (not word_2) and (not next_word):
                    try:
                        word_2 = random.choice(self.bi_lexicon[seed])
                        bigram = "{} {}".format(seed, word_2)
                        next_word = random.choice(self.tri_lexicon[bigram])
                    except KeyError:
                        bad_sentence = True
                        break
                if bad_sentence:
                    break
                if word_2 not in self.stop_puncts:
                    candidate_sentence.append(word_2)
                bigram = "{} {}".format(word_2, next_word)
                seed = word_2
                if (next_word in self.stop_puncts) or (next_word not in self.bi_lexicon):
                    response_candidates.append(" ".join(candidate_sentence))
                    break
        return response_candidates

    def compose_response(self, input_sent, input_filter, output_filter, lexicon=None):
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
        chains = self._create_chains(seed)
        # Return output of filter
        return output_filter(chains)


if __name__ == '__main__':
    bot = Chatbot()
    bot.fill_lexicon()
    print "Filled the lexicon!"
    print bot.compose_response("My beautiful carriage is red and blue and it hums while I drive it!",
        input_filters.filter_content_priority, bot.o_filter_random, bot.bi_lexicon)


