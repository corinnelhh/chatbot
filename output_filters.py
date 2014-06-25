import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize

funct_dict = {}


def add_func_to_dict(func):
    funct_dict[func.__name__] = func
    return func


@add_func_to_dict
def filter_length(sentences, wordcount=13):
    """Takes in a list of sentences and returns a reduced list,

    that contains only sentences with less than <wordcount> words."""

    for sentence in sentences[:]:
        if len(sentence.split()) > wordcount:
            sentences.remove(sentence)
    return sentences


@add_func_to_dict
def filter_pos(sentences):
    """Takes in a list of sentences and returns a reduced list,

    that contains only sentences that contain the necessarry pos."""
    content_pos = ['VB', 'NN', 'JJ']
    output_sentences = []
    for sentence in sentences:
        words = wordpunct_tokenize(sentence)
        tagged = pos_tag(words)
        for word, pos in tagged:
            if pos[:2] in content_pos:
                output_sentences.append(sentence)
                break
    return output_sentences


@add_func_to_dict
def filter_NN_VV(sentences):
    """Takes in a list of sentences and returns a reduced list of
    sentences that have at least one noun followed somewhere by at least
    one verb.
    """
    output_sentences = []
    for sentence in sentences:
        words = wordpunct_tokenize(sentence)
        tagged = pos_tag(words)
        for word, tag in tagged:
            has_noun = False
            if tag[:2] == "NN":
                has_noun = True
            if has_noun and tag[:2] == "VB":
                output_sentences.append(sentence)
                break
    return output_sentences
