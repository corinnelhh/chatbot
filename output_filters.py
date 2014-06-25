import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
from collections import OrderedDict

funct_dict = OrderedDict({})


def add_func_to_dict(name=None):
    def wrapper(func):
        function_name = name
        if function_name is None:
            function_name = func.__name__
        funct_dict[function_name] = func
        return func
    return wrapper


@add_func_to_dict("No Filter Selected")
def no_o_filter_selected(sentences):
    return sentences


@add_func_to_dict("Length Filter")
def filter_length(sentences, wordcount=13):
    """Takes in a list of sentences and returns a reduced list,
    that contains only sentences with less than <wordcount> words."""
    output_sentences = []
    for sentence in sentences[:]:
        sentence = sentence.split()[:wordcount]
        output_sentences.append(" ".join(sentence))
    return output_sentences


@add_func_to_dict("Part of Speech Filter")
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


@add_func_to_dict("Noun-Verb Filter")
def filter_NN_VV(sentences):
    """Takes in a list of sentences and returns a reduced list of
    sentences that have at least one noun followed somewhere by at least
    one verb.
    """
    output_sentences = []
    for sentence in sentences:
        words = wordpunct_tokenize(sentence)
        tagged = pos_tag(words)
        has_noun = False
        for word, tag in tagged:
            if tag[:2] == "NN":
                has_noun = True
            if has_noun and tag[:2] == "VB":
                output_sentences.append(sentence)
                break
    return output_sentences
