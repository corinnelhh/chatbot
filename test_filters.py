import input_filters
import output_filters
import chatbot_brain
from nltk.tokenize import wordpunct_tokenize

#input filters start here


def test_small_talk_filter():
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    tester = wordpunct_tokenize("raining snowing sunny weather")
    weather_opts = ["Talking about the weather is such a bore.",
        "I'm not the weatherman!"]
    sentence = input_filters.filter_small_talk(tester, bot.bi_lexicon)
    assert sentence in weather_opts


def test_filter_content():
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    tester = wordpunct_tokenize("The young boy ran quickly through the woods.")
    seeds = input_filters.filter_content(tester, bot.bi_lexicon)
    assert "young" in seeds
    assert "boy" in seeds
    assert "woods" in seeds
    assert "ran" in seeds
    assert "quickly" not in seeds
    assert "the" not in seeds


def test_filter_length_words():
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    tester = wordpunct_tokenize("I am not happy but I am not hungry either.")
    seeds = input_filters.filter_length_words(tester, bot.bi_lexicon)
    assert "I" not in seeds
    assert "hungry" in seeds
    assert "happy" in seeds
    assert "am" not in seeds


def test_filter_content_priority():
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    tester = wordpunct_tokenize("Children look happy.")
    seeds = input_filters.filter_content_priority(tester, bot.bi_lexicon)
    assert "children" in sorted(seeds)[:3]
    assert "look" not in sorted(seeds)[:3]
    assert "look" in sorted(seeds)[3:5]
    assert "children" not in sorted(seeds)[3:5]
    assert "happy" in sorted(seeds)[5:]

#output filters start here

sentences = ["good breeding and of the match Lady Catherine is not know and let us the express To morrow fortnight and by any thing in a month You see it and sometimes made the very gravely glancing.",
            "here are to the company I congratulate you have seen Collins and he had recommended him from Jane I dare say",
            "hello my friend I hope you are well",
            "good evening gracious lady you are most considerate",
            "may I entertain you with a list of seasonal chocolates",
            "perhaps your kindness shall be rewarded"]


def test_length():
    reduced_sentences = output_filters.filter_length(sentences)
    assert len(reduced_sentences) == 4


def test_length_null():
    reduced_sentences = output_filters.filter_length(sentences)
    same_sentences = output_filters.filter_length(reduced_sentences)
    assert len(same_sentences) == len(reduced_sentences)


def test_filter_pos():
    sentences = ["good breeding and of the match Lady Catherine is not know and let us the express To morrow fortnight and by any thing in a month You see it and sometimes made the very gravely glancing.",
            "here are to the company I congratulate you have seen Collins and he had recommended him from Jane I dare say",
            "hello my friend I hope you are well",
            "good evening gracious lady you are most considerate",
            "may I entertain you with a list of seasonal chocolates",
            "perhaps your kindness shall be rewarded"]
    reduced_sentences = output_filters.filter_pos(sentences)
    assert len(reduced_sentences) == 6


