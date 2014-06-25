import nltk
from nltk import pos_tag
from nltk.tokenize import wordpunct_tokenize
import random

input_funcs = {}


def add_func_to_dict(name=None):
    def wrapper(func):
        function_name = name
        if function_name is None:
            function_name = func.__name__
        input_funcs[function_name] = func
        return func
    return wrapper


@add_func_to_dict("Small Talk Filter")
def filter_small_talk(input_, lexicon=None):
    sports_words = ["basketball", "soccer", "football",
                    "baseball", "hockey", "tennis"]
    weather_words = ["weather", "raining", "rain", "snowing",
                     "snows", "sunny", "cloudy"]
    feeling_words = ["happy", "sad", "lonely", "excited"]
    if input_[:2] == ["It", "means"]:
        return small_talk_dict('new_word')
    for word in input_:
        if word in sports_words:
            return small_talk_dict('sports')
        elif word in weather_words:
            return small_talk_dict('weather')
        elif word in feeling_words:
            return small_talk_dict('feelings')
        # elif word not in lexicon:
        #    return small_talk_dict('unknown_word')
    else:
        return input_


def small_talk_dict(dict_key):
    """
    Takes in a dictkey and an optional keyword. Sentences are randomly
    selected from the list of values. If a keyword is present,
    keyword is added into the output string.
    """

    dict_ = {
        'unknown_word': [
            "What a funny thing to say!",
            "That's a new one!",
            "Huh!"
            ],
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
        'new_word': [
            'Wow, thanks for explaining that.'
            ]
        }

    return random.choice(dict_[dict_key])


def token(string_):
    return wordpunct_tokenize(string_)


@add_func_to_dict("Content Filter")
def filter_content(words):
    """Takes in a list of words and returns a list

    of the nouns, verbs, and adjectives the orig list contained."""
    tagged = pos_tag(words)
    possible_seeds = []
    content_pos = ['VB', 'NN', 'JJ']
    for word, pos in tagged:
        if pos[:2] in content_pos:
            possible_seeds.append(word)
    return possible_seeds


@add_func_to_dict("Length Filter")
def filter_length_words(words):
    "Takes in a list of words and returns all words longer than two letters."
    possible_seeds = []
    for word in words:
        if len(word) > 2:
            possible_seeds.append(word)
    return possible_seeds


@add_func_to_dict("Noun > Verb > Adjective Filter")
def filter_content_priority(words):
    "Takes in a list of words and returns words with 'weighted' priorities"
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

print "heloo"
