import nltk
import random
import os
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
import pdb


class Trainbot(object):
    def __init__(self):
        self.tri_lexicon = {}
        self.bi_lexicon = {}
        self.pos_lexicon_word_pos = {}
        self.pos_lexicon_pos_word = {}
        self.stop_puncts = ['.', '!', '?']
        self.puncts = [',', ';', ':', '"', "'", '-', '--', ",?", '."',',"',
        "Mr", "Mrs", '?"']

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

    def _pos_lexicons(self, training_file):
        """Creates two pos dictionaries.

        One with every word as a key and the values being a list of all it's parts of speech.
        The list may look like [noun,verb,noun,noun] implying that it
        is a noun more often than a verb. The second is the same, but inverted."""

        f = open(training_file)
        print "opened PART OF SPEECH DICT"
        counter = 0
        for words in self.parse_training_input(f):
            tagged = pos_tag(words)
            for word, pos in tagged:
                counter += 1
                if word in self.pos_lexicon_word_pos:
                    self.pos_lexicon_word_pos[word].append(pos)
                else:
                    self.pos_lexicon_word_pos[word] = [pos]
                if pos in self.pos_lexicon_pos_word:
                    self.pos_lexicon_pos_word[pos].append(word)
                else:
                    self.pos_lexicon_pos_word[pos] = [word]
            print "Building dict..." + str(counter)
        print "Done with POS DICT"

        # return len(self.pos_lexicon_word_pos), self.pos_lexicon_pos_word

    def _fill_lexicon(self, training_file):
        f = open(training_file)
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

    def generate_pos_dict(self, training_file, prefix):
        self._pos_lexicons(training_file)

        training_dict_file = "%s/%s_word_pos_dict.txt" % (prefix, prefix)
        dict_text = open(training_dict_file, 'w')
        dict_text.write(str(tb.pos_lexicon_word_pos))

        training_dict_file = "%s/%s_pos_word_dict.txt" % (prefix, prefix)
        dict_text = open(training_dict_file, 'w')
        dict_text.write(str(tb.pos_lexicon_pos_word))

    def generate_gram_dict(self, training_file, prefix):
        self._fill_lexicon(training_file)

        training_dict_file = "%s/%s_bi_gram_dict.txt" % (prefix, prefix)
        dict_text = open(training_dict_file, 'w')
        dict_text.write(str(tb.bi_lexicon))

        training_dict_file = "%s/%s_tri_gram_dict.txt" % (prefix, prefix)
        dict_text = open(training_dict_file, 'w')
        dict_text.write(str(tb.tri_lexicon))

    def generate_all_dicts(self, training_file):
        prefix = str(training_file)[:-4]
        if not os.path.exists(prefix):
            os.makedirs(prefix)
        self.generate_gram_dict(training_file, prefix)
        self.generate_pos_dict(training_file, prefix)
        os.rename(training_file, "%s/%s" % (prefix, training_file))


if __name__ == '__main__':
    tb = Trainbot()
    tb.generate_all_dicts('quickTest.txt')
