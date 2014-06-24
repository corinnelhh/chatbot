import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

def token(string_):
    return wordpunct_tokenize(string_)

def filter_content(words):
    """Takes in a list of words and returns a list

    of the nouns, verbs, and adjectives the orig list contained."""
    tagged = pos_tag(words)
    possible_seeds = []
    content_pos = ['VV','NN','JJ']
    for word,pos in tagged:
        if pos[:2] in content_pos:
            possible_seeds.append(word)
    return possible_seeds


def filter_length_words(words):
    """Takes in a list of words and returns all words longer than two letters."""
    possible_seeds = []
    for word in words:
        if len(word) >2:
            possible_seeds.append(word)
    return possible_seeds


if __name__ == '__main__':
    print filter_content(token("I went running yesterday"))
