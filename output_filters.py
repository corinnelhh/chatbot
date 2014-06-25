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



