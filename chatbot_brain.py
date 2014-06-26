#import nltk
import random
#import os
#from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
from collections import OrderedDict

from trainbot import Trainbot
import input_filters
import output_filters
import brains


class Chatbot(Trainbot):

    def __init__(self, training_file="tell_tale_heart.txt"):
        super(Chatbot, self).__init__(training_file="tell_tale_heart.txt")
        self.training_file = training_file
        self.sausage = {}

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
        u"""Return randomly selected sentence from sentences"""
        return random.choice(sentences)

    def output_filtration(self, output_filter, chains):
        if u"No Filter Selected" not in output_filter:
            all_filters = []
            for _filter in output_filter:
                all_filters.append(output_filters.funct_dict[_filter])
            filtered, report = self._chain_filters(chains, all_filters)
            self.sausage["o_filter_report"] = report
            if len(filtered) > 0:
                output = self.o_filter_random(filtered)
            else:
                output = "I'm not sure what to say about that."
        else:
            output = self.o_filter_random(chains)
        return output

    def sanitize_seeds(self, seeds):
        """returns only seeds that are in the lexicons"""

        for seed in seeds[:]:
            try:
                self.bi_lexicon[seed]
            except KeyError:
                seeds.remove(seed)
        return seeds

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
                print "seed not in lexicon"
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

    def _make_sausage(self):
        """compiles a report on how the reply was made"""
        message = OrderedDict({})
        message["final_sentence"] = """<h4>This is how the response <i>\
        '{final_sentence}'</i> was made:</h4>""".format(**self.sausage)
        if "input_filter" in self.sausage:
            i_filters = []
            for _filter in self.sausage["input_filter"]:
                if _filter != "No Filter Selected":
                    i_filters.append(_filter)
            if len(i_filters) > 0:
                self.sausage["applied_i_filters"] = i_filters
        if "applied_i_filters" in self.sausage:
            message["input_filter"] = """
            <p> With the {input_filter} input filter, <i>{final_seed}</i>\
             was chosen as the 'seed word' for our Markov Chain sentence\
             generator. <p>""".format(**self.sausage)
        if "first_bigram" in self.sausage:
            message["first_bigram"] = """<p>Then we used bigram probability\
             to pick <i>{first_bigram}</i> as the first pair of words to\
              feed our Markov Chain sentence generator.</p>""".format(**self.sausage)
        else:
            message["no_bigram"] = """<p> A lexicon search did not return\
            a likely next word, so a default response <i>{final_sentence}</i>\
            was returned. </p>""".format(**self.sausage)
        if "unfiltered_chains" in self.sausage:
            message["unfiltered_chains"] = """<p> After feeding in \
            <i>{first_bigram}</i>, the Markov Chain sentence generator\
            returned some sentences.</p>""".format(**self.sausage)
        #if "o_filter_report" in self.sausage:
            #for item in self.sausage["o_filter_report"]:

            #message["number_filters"] =


           # len(self.sausage["o_filter_report"])

            #message["output_filters"] = """<p>The sentences were fed through\
            # these filters: {output_filters} </p>""".format(**self.sausage)
        return message

    def compose_response(
            self,
            input_sent,
            input_key,
            output_filter,
            brain
            ):
        u"""Return a response sentence and report based on the input."""
        seeds = wordpunct_tokenize(input_sent)
        seeds = input_filters.input_funcs[input_key](seeds)
        seeds = self.sanitize_seeds(seeds)
        if len(seeds) == 0:
            return "You speak nothing but nonsense."
        chains = brains.brain_dict[brain](self, seeds)
        output = self.output_filtration(output_filter, chains)
        return output

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
