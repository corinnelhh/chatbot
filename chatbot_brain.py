import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
import pdb

from trainbot import Trainbot


class Chatbot(Trainbot):

    def __init__(self, training_file="tell_tale_heart.txt"):
        super(Chatbot, self).__init__()
        self.training_file = training_file

    def i_filter_random(self, words):
        count = 0
        while count < len(words):
            seed = random.choice(words)
            if (seed in self.bi_lexicon) and (seed not in self.stop_puncts):
                return seed
            count += 1
        return "What a funny thing to say!"

    def o_filter_random(self, sentences):
        return str(random.choice(sentences))

    def generate_response(self, input_sent):
        #words = self.tag_input(input_sent)
        words = wordpunct_tokenize(input_sent)
        first_seed = self.i_filter_random(words)
        if first_seed == "What a funny thing to say!":
            return first_seed
        print "Given the seed: {}".format(first_seed)
        response_candidates = []
        while len(response_candidates) < 10:
            bad_sentence = False
            seed = first_seed
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
        return self.o_filter_random(response_candidates)

# def full_package():
#     gener

if __name__ == '__main__':
    bot = Chatbot()
    bot.fill_lexicon()
    print "Filled the lexicon!"
    print bot.generate_response("How are you doing?")
