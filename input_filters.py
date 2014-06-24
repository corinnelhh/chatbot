import nltk
from nltk.tokenize import wordpunct_tokenize
import random


def i_filter_small_talk_typer(input_):
    if wordpunct_tokenize(input_)[:2] == ["It", "means"]
        return i_filter_small_talk('new_word')
    elif "weather" in input_:
        return 'weather'
    else:
        return _input


def i_filter_small_talk(dict_key, keyword=None):
    """
    Takes in a dictkey and an optional keyword. Sentences are randomly
    selected from the list of values. If a keyword is present,
    keyword is added into the output string.
    """

    small_talk_dict = {'unknown_word' : ["What a funny thing to say!",
        "That's a new one!", "Huh!"],'weather' :
        ["Talking about the weather is such a bore.",
        "I'm not the weatherman!"], 'feelings' :
        ["Why do you care how I feel?",
        "More importantly, how do you feel?",
        "Really, are *you* {}".format()],
        'sports' : ["You're a sports fan!",
        "I've never been much of an athlete..."],
        'new_word': ['Wow, thanks for explaining that.',
    }

    while True:
        response = random.choice(small_talk_dict[dict_key])
        if 


if __name__ == "__main__":

