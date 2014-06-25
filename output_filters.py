import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize


def filter_length(sentences, wordcount=13):
    """Takes in a list of sentences and returns a reduced list,

    that contains only sentences with less than <wordcount> words."""

    for sentence in sentences[:]:
        if len(sentence.split())>wordcount:
            sentences.remove(sentence)
    return sentences


def filter_pos(sentences):
    """Takes in a list of sentences and returns a reduced list,

    that contains only sentences that contain the necessarry pos."""
    content_pos = ['VB','NN','JJ']
    output_sentences = []
    for sentence in sentences:
        words = wordpunct_tokenize(sentence)
        tagged = pos_tag(words)
        for word, pos in tagged:
            if pos[:2] in content_pos:
                output_sentences.append(sentence)
                break
    return output_sentences

def filter_NN_VV(sentences):
    """Takes in a list of sentences and returns a reduced list of
    sentences that have at least one noun followed somewhere by at least one verb
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




