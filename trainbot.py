import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
import pdb


class Trainbot(object):
    def __init__(self, training_file="tell_tale_heart.txt"):
        self.training_file = training_file
        self.tri_lexicon = {}
        self.bi_lexicon = {}
        self.pos_lexicon_word_pos = {}
        self.pos_lexicon_pos_word = {}
        self.stop_puncts = ['.', '!', '?']
        self.puncts = [',', ';', ':', '"', "'", '-', '--', ",?", '."',',"']

    def parse_training_input(self, text):
        while True:
            our_text = text.read(20048)
            if not our_text:
                break
            yield wordpunct_tokenize(our_text)

    def remove_non_final_punctuation(self, our_list):
        for i in our_list[:]:
            if i in self.puncts:
                our_list.remove(i)
        return our_list

    def tag_input(self, our_string):
        our_string = wordpunct_tokenize(our_string)
        return pos_tag(our_string)


    def pos_lexicons(self):
        """Creates two pos dictionaries.

        One with every word as a key and the values being a list of all it's parts of speech.
        The list may look like [noun,verb,noun,noun] implying that it
        is a noun more often than a verb. The second is the same, but inverted."""

        f = open(self.training_file)
        print "opened"
        for words in self.parse_training_input(f):
            tagged = pos_tag(words)
            for word, pos in tagged:
                if word in self.pos_lexicon_word_pos:
                    self.pos_lexicon_word_pos[word].append(pos)
                else:
                    self.pos_lexicon_word_pos[word] = [pos]

                if pos in self.pos_lexicon_pos_word:
                    self.pos_lexicon_pos_word[pos].append(word)
                else:
                    self.pos_lexicon_pos_word[pos] = [word]
                if len(self.pos_lexicon_word_pos)>20:
                    return len(self.pos_lexicon_word_pos), self.pos_lexicon_pos_word


    def fill_lexicon(self):
        f = open(self.training_file)
        for words in self.parse_training_input(f):
            words = self.remove_non_final_punctuation(words)
            for idx, word in enumerate(words[2:]):
                word_pair = "{} {}".format(words[idx], words[idx + 1])
                first_word = str(words[idx])
                second_word = str(words[idx + 1])
                if first_word not in self.bi_lexicon:
                    self.bi_lexicon[first_word] = [second_word]
                if word_pair not in self.tri_lexicon:
                    self.tri_lexicon[word_pair] = [word]
                else:
                    self.bi_lexicon[first_word].append(second_word)
                    self.tri_lexicon[word_pair].append(word)
