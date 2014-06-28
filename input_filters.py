import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
import random
from collections import OrderedDict

input_funcs = OrderedDict({})


def add_func_to_dict(name=None):
    def wrapper(func):
        function_name = name
        if function_name is None:
            function_name = func.__name__
        input_funcs[function_name] = func, func.__doc__
        return func
    return wrapper


@add_func_to_dict("No Filter Selected")
def no_input_filter_selected(input_):
    u"""All words in the input are passed
    through to be checked against the lexicon."""
    return input_


@add_func_to_dict("Small Talk Filter")
def filter_small_talk(input_):
    u"""Sentences containing certain keywords
    (such as 'raining' or 'football') return a
    hard-coded response rather than a response
    generated in the 'brain'."""
    sports_words = ["basketball", "soccer", "football",
                    "baseball", "hockey", "tennis"]
    weather_words = ["weather", "raining", "rain", "snowing",
                     "snows", "sunny", "cloudy"]
    feeling_words = ["happy", "sad", "lonely", "excited"]

    for word in input_:
        if word in sports_words:
            return small_talk_dict('sports'), word
        elif word in weather_words:
            return small_talk_dict('weather'), word
        elif word in feeling_words:
            return small_talk_dict('feelings'), word
    else:
        return input_


def small_talk_dict(dict_key):
    """
    Takes in a dictkey. Sentences are randomly
    selected from the list of values.
    """

    dict_ = {
        'weather': [
            "Talking about the weather is such a bore.",
            "I'm not the weatherman!"
            ],
        'feelings': [
            "Feelings are so complicated.",
            "It's good to know how you feel."
            ],
        'sports': [
            "You're a sports fan!",
            "I've never been much of an athlete..."
            ],
        }
    return random.choice(dict_[dict_key])


def token(string_):
    return wordpunct_tokenize(string_)


@add_func_to_dict("Content Filter")
def filter_content(words):
    u"""Only 'content words' (here, nouns, verbs,
    and adjectives) are passed along as seed words
    for the brain to generate sentences."""
    tagged = pos_tag(words)
    possible_seeds = []
    content_pos = ['VB', 'NN', 'JJ']
    for word, pos in tagged:
        if pos[:2] in content_pos:
            possible_seeds.append(word)
    return possible_seeds


@add_func_to_dict("Length Filter")
def filter_length_words(words):
    u"""Only words longer than 2 characters are passed
    along as seed words for the brain to generate sentences."""
    possible_seeds = []
    for word in words:
        if len(word) > 2:
            possible_seeds.append(word)
    return possible_seeds


@add_func_to_dict("Noun > Verb > Adjective Filter")
def filter_content_priority(words):
    u"""Only 'content words' (here, nouns, verbs,
    and adjectives) are passed along as seed words
    for the brain to generate sentences; words are
    given weighted priorities with nouns > verbs > adjectives."""
    tagged = pos_tag(words)
    possible_seeds = []
    for word, pos in tagged:
        if pos[:2] == 'NN':
            possible_seeds.append(word)
            possible_seeds.append(word)
            possible_seeds.append(word)
        elif pos[:2] == 'VB':
            possible_seeds.append(word)
            possible_seeds.append(word)
        elif pos[:2] == 'JJ':
            possible_seeds.append(word)
    return possible_seeds
