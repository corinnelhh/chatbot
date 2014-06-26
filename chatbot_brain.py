#import nltk
import random
#import os
#from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

from trainbot import Trainbot
import input_filters
import output_filters


class Chatbot(Trainbot):

    def __init__(self, training_file=u"tell_tale_heart.txt"):
        super(Chatbot, self).__init__(training_file=u"tell_tale_heart.txt")
        self.training_file = training_file

    def i_filter_random(self, words, lexicon=None):
        u"""Return randomly selected, non-punctuation word from words."""
        count = 0
        while count < len(words):
            seed = random.choice(words)
            if (seed in self.bi_lexicon) and (seed not in self.stop_puncts):
                return seed
            count += 1
        return u"What a funny thing to say!"

    def o_filter_random(self, sentences):
        u"""Return randomly selected sentence from sentecnces"""
        if len(sentences) > 0:
            return random.choice(sentences)
        else:
            return u"I'm not sure what to say about that."

    def _create_chains(self, pair, size=10):
        u"""Return list of markov generated strings spawned from the seed."""
        candidates = []
        w_1 = pair[0]
        w_2 = pair[1]
        while len(candidates) < size:
            word_1, word_2 = w_1, w_2
            candidate = [word_1, word_2]
            pair = u"{} {}".format(word_1, word_2)
            done = False
            while not done:
                try:
                    next_word = random.choice(self.tri_lexicon[pair])
                    candidate.append(next_word)
                    word_1, word_2 = word_2, next_word
                    pair = u"{} {}".format(word_1, word_2)
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

    def _chain_filters(self, strings, filters):
        u"""Return a list of strings that satisfiy the requirements of all filters.

        Expects: A list of filter functions.
        Returns: A list of strings.
        """
        strings, output_dict = self._filter_recursive(strings, filters)
        return strings, output_dict

    def _filter_recursive(self, strings, filters, output_dict={}):
        u"""Return list of strings or call the next filter function."""
        if filters == []:
            return strings, output_dict
        else:
            output_dict[filters[0].__name__] = filters[0](strings)
            return self._filter_recursive(
                filters[0](strings),
                filters[1:],
                output_dict
                )

    def apply_o_filter(self, filter_, chains):
        if filter_ == u"filter_length":
            return output_filters.filter_length(chains)
        if filter_ == u"filter_pos":
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
        sausage = {}
        sausage["submission"] = input_sent
        seeds = wordpunct_tokenize(input_sent)
        sausage["input_words"] = seeds
        # Select seed based on input filter
        if input_key:
            sausage["input_filter"] = input_key
            print u"Input filter: {}".format(input_key)
            seeds = input_filters.input_funcs[input_key](seeds)
            sausage["final_seeds"] = seeds
            if isinstance(seeds, basestring):
                return seeds
        # Randomly pick a seed from the returned possibilities.
        print seeds
        seed = self.i_filter_random(seeds)
        sausage["final_seed"] = seed
        if seed == u"What a funny thing to say!":
            return seed
        # Create chains
        pair = self._pair_seed(seed)
        sausage["first_bigram"] = pair
        chains = self._create_chains(pair)
        sausage["unfiltered_chains"] = chains
        # Return output of filter
        if output_filter != "default":
            print u"Output filter: {}".format(output_filter)
            filtered = output_filters.funct_dict[output_filter](chains)
        else:
            output = chains
        output = self.o_filter_random(filtered)
        return output, sausage

if __name__ == u'__main__':
    bot = Chatbot(training_file="Doctorow.txt")
    bot.fill_lexicon()
    print u"Filled the lexicon!"
    print bot.compose_response(
        u"My beautiful carriage is red and blue and it hums while I drive it!",
        u"Content Filter",
        u"Noun-Verb Filter"
        )
    strings = bot._create_chains(bot._pair_seed('car'))
    filters = [output_filters.funct_dict["Length Filter"], output_filters.funct_dict["Noun-Verb Filter"]]
