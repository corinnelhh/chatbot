import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
from collections import OrderedDict
import random

funct_dict = OrderedDict({})

grammar1 = nltk.parse_cfg("""
    Sent  -> NP VP | NP VP END
    NP -> Det Nom | PropN | Det NP | N | PR | PR Nom
    Nom -> Adj Nom | N
    VP -> V Adj | V NP | V S | V NP PP | V Prep NP | V | V CC V
    PP -> Prep NP

    PropN -> 'NNP' | 'NNPS'
    Det -> 'DT'
    N -> 'NN' | 'NNS'
    Adj  -> 'JJ' | 'JJR' |  'JJS'
    V ->  'VB'  | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ'
    Prep -> 'TO' | 'IN'
    CC -> 'CC'
    PR -> 'PRP' | 'PRP$'
    RB -> 'RB' | 'RBR' | 'RBS'
    END -> '.' | '?' | '!'
    """)


def add_func_to_dict(name=None):
    def wrapper(func):
        function_name = name
        if function_name is None:
            function_name = func.__name__
        funct_dict[function_name] = func, func.__doc__
        return func
    return wrapper


@add_func_to_dict("No Filter Selected")
def no_o_filter_selected(sentences, bot_dict):
    u"""All generated sentences are passed along for
    random selection."""
    return sentences


@add_func_to_dict("Length Filter")
def filter_length(sentences, bot_dict):
    u"""Only sentences with a length <= 8 are passed
    along for random selection."""
    wordcount = 8
    output_sentences = []
    for sentence in sentences[:]:
        sentence = sentence.split()
        if len(sentence) <= wordcount:
            output_sentences.append(" ".join(sentence))
    return output_sentences


@add_func_to_dict("Part of Speech Filter")
def filter_pos(sentences, bot_dict):
    u"""Only sentences containing at least one
    verb, noun, or adjective are passed along
    for random selection."""
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
def filter_NN_VV(sentences, bot_dict):
    u"""Only sentences containing at least one noun followed
    somewhere by at least one verb are passed along for
    random selection."""
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


@add_func_to_dict("Noun-Verb-Noun Filter")
def weak_syntactic_filter(sentences, bot_dict):
    u"""Only sentences containing at least one noun followed
    somewhere by at least one verb followed by at least one
    noun are passed along for random selection."""
    output_sentences = []
    noms = ["NN", "PR"]
    print "first we had {} sentences.".format(len(sentences))
    for sentence in sentences:
        has_NN = False
        has_VV = False
        passes = False
        tagged_tokens = pos_tag(wordpunct_tokenize(sentence))
        print tagged_tokens
        for word, tag in tagged_tokens:
            if tag[:2] in noms:
                has_NN = True
            if has_NN and tag[:2] == "VB":
                has_VV = True
            if has_NN and has_VV and tag[:2] in noms:
                passes = True
        if passes:
            output_sentences.append(sentence)
            print "*************"
            print sentence
    print "Then we had {} sentences".format(len(output_sentences))
    return output_sentences


@add_func_to_dict("Syntactic Filter Fast")
def syntactic_filter_fast(sentences, bot_dict):
    u"""Only sentences with an underlying structure
    matching a given content-free grammar are passed
    along for random selection. Filters responses
    through looking up the part of speech for input words
    in a local lexicon and recursively mapping
    phrase structures."""
    output_sentences = []
    print "Before syntax filter there were " + str(len(sentences)) + " sentences."
    for sentence in sentences:
        print "=================="
        print str(sentence) + "\n"
        tokens = nltk.tokenize.wordpunct_tokenize(sentence)
        justTags = []
        # print self.pos_lexicon_word_pos
        for word in tokens[:-1]:
            tag = random.choice(bot_dict[word])
            justTags.append(tag)
        justTags.append(tokens[-1])
        print str(justTags) + "\n"
        rd_parser = nltk.RecursiveDescentParser(grammar1)
        try:
            if len(rd_parser.nbest_parse(justTags)) > 0:
                output_sentences.append(sentence)
        except ValueError:
            pass
    print "After the syntax filter there were " + str(len(output_sentences)) + " sentences."
    print output_sentences
    return output_sentences


@add_func_to_dict("Syntactic Filter")
def syntactic_filter(sentences, bot_dict):
    u"""Only sentences with an underlying structure
    matching a given content-free grammar are passed
    along for random selection. Filters responses
    through part of speech tagging and
    recursive structure lookup."""
    output_sentences = []
    print "Before syntax filter there were " + str(len(sentences)) + " sentences."
    for sentence in sentences:
        print "=================="
        print str(sentence) + "\n"
        tokens = nltk.tokenize.wordpunct_tokenize(sentence)
        posTagged = nltk.pos_tag(tokens)
        justTags = []
        for word, tag in posTagged:
            justTags.append(tag)
        print str(justTags) + "\n"
        rd_parser = nltk.RecursiveDescentParser(grammar1)
        try:
            if len(rd_parser.nbest_parse(justTags)) > 0:
                output_sentences.append(sentence)
        except ValueError:
            pass
    print "After the syntax filter there were " + str(len(output_sentences)) + " sentences."
    print output_sentences
    return output_sentences



