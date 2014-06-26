#import nltk
import random
#import os
#from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
from collections import OrderedDict

from trainbot import Trainbot
import input_filters
import output_filters


class Chatbot(Trainbot):

    def __init__(self, training_file="tell_tale_heart.txt"):
        super(Chatbot, self).__init__(training_file="tell_tale_heart.txt")
        self.training_file = training_file

    def i_filter_random(self, words):
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

    def _make_sausage(self, sausage):
        """compiles a report on how the reply was made"""
        message = OrderedDict({})
        message["final_sentence"] = """<h5>This is how the response <i>\
        '{final_sentence}'</i> was made:</h5>""".format(**sausage)
        if "input_filter" in sausage:
            i_filters = []
            for _filter in sausage["input_filter"]:
                if _filter != "No Filter Selected":
                    i_filters.append(_filter)
            if len(i_filters) > 0:
                sausage["applied_i_filters"] = i_filters
        if "applied_i_filters" in sausage:
            message["input_filter"] = """
            <p> With the {input_filter} input filter, <i>{final_seed}</i>\
             was chosen as the 'seed word' for our Markov Chain sentence\
             generator. <p>""".format(**sausage)
        if "first_bigram" in sausage:
            message["first_bigram"] = """<p>Then we used bigram probability\
             to pick <i>{first_bigram}</i> as the first pair of words to\
              feed our Markov Chain sentence generator.</p>""".format(**sausage)
        return message

    def compose_response(
            self,
            input_sent,
            input_key=None,
            output_filter=None,
            ):
        u"""Return a response sentence and report based on the input."""
        # Tokenize input
        sausage = {}
        report = ""
        seeds = wordpunct_tokenize(input_sent)
        # Select seed based on input filter
        if input_key:
            sausage["input_filter"] = input_key
            seeds = input_filters.input_funcs[input_key](seeds)
            #sausage["final_seeds"] = seeds
        if not isinstance(seeds, basestring):
            # Randomly pick a seed from the returned possibilities.
            seed = self.i_filter_random(seeds)
            sausage["final_seed"] = seed
            if seed != "What a funny thing to say!":
                # Create chains
                pair = self._pair_seed(seed)
                sausage["first_bigram"] = " ".join(pair)
                chains = self._create_chains(pair)
                sausage["unfiltered_chains"] = chains
                sausage["chain_length"] = len(chains)
                filled_filters = []
                for _filter in output_filter:
                    if _filter != "No Filter Selected":
                        filled_filters.append(_filter)
                sausage["output_filters"] = ",".join(filled_filters)
                if output_filter != "default":
                    #import pdb; pdb.set_trace()
                    all_filters = []
                    for _filter in output_filter:
                        all_filters.append(output_filters.funct_dict[_filter])
                    filtered, report = self._chain_filters(chains, all_filters)
                    sausage["o_filter_report"] = report
                else:
                    output = chains
                if len(filtered) > 0:
                    output = self.o_filter_random(filtered)
                else:
                    output = "I'm not sure what to say about that."
            else:
                output = seed
        else:
            output = seeds
        sausage["final_sentence"] = output
        sausage = self._make_sausage(sausage)
        return output, sausage

if __name__ == '__main__':
    bot = Chatbot(training_file="Doctorow.txt")
    bot.fill_lexicon()
    print "Filled the lexicon!"
    print bot.compose_response(
        "My beautiful carriage is red and blue and it hums while I drive it!",
        "Content Filter",
        "Noun-Verb Filter"
        )
    strings = bot._create_chains(bot._pair_seed('car'))
    filters = [output_filters.funct_dict["Length Filter"], output_filters.funct_dict["Noun-Verb Filter"]]
