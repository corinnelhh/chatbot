import nltk
from nltk.tokenize import wordpunct_tokenize
import random
from trainbot import Trainbot


def i_filter_small_talk_typer(input_):
    bot = Trainbot()
    bot.fill_lexicon()
    print "That's the length of the lexicon"
    print len(bot.bi_lexicon)
    sports_words = ["basketball", "soccer", "football", "baseball",
            "hockey", "tennis"]
    weather_words = ["weather", "raining", "rain", "snowing", "snows",
            "sunny", "cloudy"]
    feeling_words = ["happy", "sad", "lonely", "excited"]
    if input_[:2] == ["It", "means"]:
        return i_filter_small_talk('new_word')
    for word in input_:
        if word in sports_words:
            return i_filter_small_talk('sports')
        elif word in weather_words:
            return i_filter_small_talk('weather')
        elif word in feeling_words:
            return i_filter_small_talk('feelings')
        elif word not in bot.bi_lexicon:
            return i_filter_small_talk('unknown_word')
    else:
        no_small = True
        return input_, no_small


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
        ["Feelings are so complicated.",
        "It's good to know how you feel."],
        'sports' : ["You're a sports fan!",
        "I've never been much of an athlete..."],
        'new_word': ['Wow, thanks for explaining that.']
        }

    return random.choice(small_talk_dict[dict_key])



if __name__ == "__main__":
    tokenized = wordpunct_tokenize("How old are you?")
    print i_filter_small_talk_typer(tokenized)

