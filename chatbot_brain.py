import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

from trainbot import Trainbot
import input_filters
import output_filters


class Chatbot(Trainbot):

    def __init__(self, training_file="tell_tale_heart.txt"):
        super(Chatbot, self).__init__(training_file="tell_tale_heart.txt")
        self.training_file = training_file
        # self.funct_dict = {"filter_content": input_filters.filter_content,
        #                   "filter_length_words": input_filters.filter_length_words,
        #                   "filter_content_priority": input_filters.filter_content_priority}

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

    def _create_chains(self, pair, size=10):
        u"""Return list of markov generated strings spawned from the seed."""
        candidates = []
        w_1 = pair[0]
        w_2 = pair[1]
        while len(candidates) < size:
            word_1, word_2 = w_1, w_2
            candidate = [word_1, word_2]
            pair = "{} {}".format(word_1, word_2)
            done = False
            while not done:
                try:
                    next_word = random.choice(self.tri_lexicon[pair])
                    candidate.append(next_word)
                    word_1, word_2 = word_2, next_word
                    pair = "{} {}".format(word_1, word_2)
                except KeyError:
                    candidates.append(" ".join(candidate))
                    done = True
                if next_word in self.stop_puncts:
                    candidates.append(" ".join(candidate))
                    done = True
        return candidates

    def _pair_seed(self, seed):
        word_1 = seed
        word_2 = None
        while word_2 is None:
            try:
                next_ = random.choice(self.bi_lexicon[seed])
                if next_ not in self.stop_puncts:
                    word_2 = next_
                    pair = [word_1, word_2]
            except KeyError:
                continue
        return pair

    # def apply_i_filter(self, filter_, seeds):
    #     lexicon = self.bi_lexicon
    #     if filter_ == "filter_content":
    #         return input_filters.filter_content(seeds)
    #     elif filter_ == "small_talk":
    #         return input_filters.filter_small_talk(seeds, lexicon)
    #     elif filter_ == "length":
    #         return input_filters.filter_length_words(seeds)
    #     elif filter_ == "content_priority":
    #         return input_filters.filter_content_priority(seeds)
    #     else:
    #         return seeds

    def apply_o_filter(self, filter_, chains):
        if filter_ == "filter_length":
            return output_filters.filter_length(chains)
        if filter_ == "filter_pos":
            return output_filters.filter_pos(chains)
        else:
            return chains

    def compose_response(
            self,
            input_sent,
            input_key=None,
            output_filter=None,
            ):
        u"""Return a response sentence based on the input."""
        # Tokenize input
        seeds = wordpunct_tokenize(input_sent)
        # Select seed based on input filter
        if input_key:
            print input_filters.funct_dict
            seeds = input_filters.funct_dict[input_key](seeds)
            if isinstance(seeds, basestring):
                return seeds
        # Randomly pick a seed from the returned possibilities.
        print seeds
        seed = self.i_filter_random(seeds)
        if seed == "What a funny thing to say!":
            return seed
        # Create chains
        pair = self._pair_seed(seed)
        chains = self._create_chains(pair)
        print chains
        # Return output of filter
        if output_filter:
            chains = self.apply_o_filter(output_filter, chains)
        chains = self.o_filter_random(chains)
        return chains

if __name__ == '__main__':
    bot = Chatbot()
    bot.fill_lexicon()
    print "Filled the lexicon!"
    print bot.compose_response(
        "My beautiful carriage is red and blue and it hums while I drive it!",
        "filter_length_words",
        bot.o_filter_random
        )
