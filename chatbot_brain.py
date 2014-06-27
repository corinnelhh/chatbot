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

    def __init__(self, training_file="Doctorow.txt"):
        super(Chatbot, self).__init__(training_file="Doctorow.txt")
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
        print "inside output_filtration"
        if u"No Filter Selected" in output_filter[0]:
            output = self.o_filter_random(chains)
        else:
            all_filters = []
            for _filter in output_filter:
                if _filter != u"No Filter Selected":
                    all_filters.append(output_filters.funct_dict[_filter])
            filtered, report = self._chain_filters(chains, all_filters)
            self.sausage["o_filter_report"] = report
            if len(filtered) > 0:
                output = self.o_filter_random(filtered)
            else:
                output = "I'm not sure what to say about that."
        return output

    def _input_filtration(self, input_sent, input_key):
        """takens an input string, passes it through any input
        filters"""
        u_seeds = wordpunct_tokenize(input_sent)
        seeds = []
        for seed in u_seeds:
            seeds.append(str(seed))
        if input_key != "No Filter Selected":
            self.sausage["input_filter"] = input_key
        filt_seeds = input_filters.input_funcs[input_key](seeds)
        self.sausage["i_filtered_seeds"] = filt_seeds
        return self.sanitize_seeds(filt_seeds)

    def sanitize_seeds(self, seeds):
        """returns only seeds that are in the lexicons"""
        for seed in seeds[:]:
            try:
                self.bi_lexicon[seed]
            except KeyError:
                seeds.remove(seed)
        self.sausage["sanitized_seeds"] = seeds
        return seeds

    def _pair_seed(self, seed):
        """identifies a pair of words to start a trigram chain"""
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
        u"""Return a list of strings that satisfiy the requirements
        of all filters.

        Expects: A list of filter functions.
        Returns: A list of strings.
        """
        strings, output_dict = self._filter_recursive(strings, filters)
        return strings, output_dict

    def _filter_recursive(self, strings, filters, output_dict=OrderedDict({})):
        u"""Return list of strings or call the next filter function."""
        print "Inside filter recursive"
        if filters == []:
            return strings, output_dict
        else:
            output_dict[filters[0].__name__] = filters[0](strings, self.word_pos)
            return self._filter_recursive(
                filters[0](strings, self.word_pos),
                filters[1:],
                output_dict
                )

    def _make_sausage(self):
        u"""compiles a report on how the reply was made"""
        message = OrderedDict({})
        message["final_sentence"] = """<h4>This is how the response <i>\
        '{final_sentence}'</i> was made:</h4>""".format(**self.sausage)
        if "input_filter" in self.sausage:
            message["input_filter"] = """
            <p> With the {input_filter} input filter, <i>{i_filtered_seeds}\
            </i> were selected. <p>""".format(**self.sausage)
        if "unfiltered_chains" in self.sausage:
            message["unfiltered_chains"] = """<p> After eliminating the \
            seed words not in the bot's'lexicon', <i>{sanitized_seeds}</i>\
            were passed to the Markov Chain sentence generator, yielding \
            200 sentences.</p>""".format(**self.sausage)
        else:
            message["no_chains"] = """<p> The seeds were next checked \
            against the bot's lexicon. The search did not return any\
             known words, so a default response <i>{final_sentence}</i>\
            was returned. </p>""".format(**self.sausage)
        if "o_filter_report" in self.sausage:
            for key, value in self.sausage["o_filter_report"].items()[::]:
                if (len(value)) > 0:
                    message[key] = """<p> Next, the sentences were passed \
                    through the {}, after which there were {} sentences \
                    remaining. </p><p> A sample sentence of what remained\
                    after this filter is: <i>{}</i>.</p>\
                    """.format(key, len(value), value[0])
        message["final_report"] = """One sentence was selected at random.\
        </p><p>And that's how the <i>{final_sentence}</i> response was\
         made!""".format(**self.sausage)
        return message

    def compose_response(
            self,
            input_sent,
            input_key,
            output_filter,
            brain
            ):
        u"""Return a response sentence and report based on the input."""
        self.sausage = {}
        seeds = self._input_filtration(input_sent, input_key)
        if len(seeds) == 0:
            output = "You speak nothing but nonsense."
        else:
            chains = brains.brain_dict[brain](self, seeds)
            self.sausage["unfiltered_chains"] = chains
            output = self.output_filtration(output_filter, chains)
        self.sausage["final_sentence"] = output
        message = self._make_sausage()
        return output, message

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
