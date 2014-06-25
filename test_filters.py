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


