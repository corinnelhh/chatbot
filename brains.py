import random
from nltk.tokenize import wordpunct_tokenize
from collections import OrderedDict
from trainbot import Trainbot
import chatbot_brain

brain_dict = OrderedDict({})

def add_func_to_dict(name=None):
    def wrapper(func):
        function_name = name
        if function_name is None:
            function_name = func.__name__
        brain_dict[function_name] = func
        return func
    return wrapper


@add_func_to_dict("Bigram Brain")
def _create_bi_chains(chatbot_brain, seeds, size=200):

    u"""Return list of markov generated strings spawned from the seed."""
    print "the seeds are: " + str(seeds)
    candidates = []
    while len(candidates) < size:
        seed = str(chatbot_brain.i_filter_random(seeds))
        candidate = [seed]
        done = False
        print "one candidate"
        while not done:
            try:
                next_word = random.choice(chatbot_brain.bi_lexicon[seed])
                candidate.append(next_word)
                seed = next_word
            except KeyError:
                candidates.append(" ".join(candidate))
                done = True
            if next_word in chatbot_brain.stop_puncts:
                candidates.append(" ".join(candidate))
                done = True
    return candidates


@add_func_to_dict("Trigram Brain")
def _create_chains(chatbot_brain, seeds, size=200):

    u"""Return list of markov generated strings spawned from the seed."""
    print "the seeds are: " + str(seeds)
    candidates = []

    while len(candidates) < size:
        seed = str(chatbot_brain.i_filter_random(seeds))
        pair = str(chatbot_brain._pair_seed(seed))
        w_1 = pair[0]
        w_2 = pair[1]
        next_word = ""
        word_1, word_2 = w_1, w_2
        candidate = [word_1, word_2]
        pair = "{} {}".format(word_1, word_2)
        done = False
        while not done:
            try:
                next_word = random.choice(chatbot_brain.tri_lexicon[pair])
                candidate.append(next_word)
                word_1, word_2 = word_2, next_word
                pair = "{} {}".format(word_1, word_2)
            except KeyError:
                candidates.append(" ".join(candidate))
                done = True
            if next_word in chatbot_brain.stop_puncts:
                candidates.append(" ".join(candidate))
                done = True
    return candidates

