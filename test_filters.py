import pytest
import input_filters
import output_filters
import chatbot_brain
from nltk.tokenize import wordpunct_tokenize
from nltk import pos_tag

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
    tester = wordpunct_tokenize("The young boy ran quickly through the woods.")
    seeds = input_filters.filter_content(tester)
    assert "young" in seeds
    assert "boy" in seeds
    assert "woods" in seeds
    assert "ran" in seeds
    assert "quickly" not in seeds
    assert "the" not in seeds


def test_filter_length_words():
    tester = wordpunct_tokenize("I am not happy but I am not hungry either.")
    seeds = input_filters.filter_length_words(tester)
    assert "I" not in seeds
    assert "hungry" in seeds
    assert "happy" in seeds
    assert "am" not in seeds


def test_filter_content_priority():
    tester = wordpunct_tokenize("Children look sleepy.")
    seeds = input_filters.filter_content_priority(tester)
    assert "Children" in sorted(seeds)[:3]
    assert "look" not in sorted(seeds)[:3]
    assert "look" in sorted(seeds)[3:5]
    assert "Children" not in sorted(seeds)[3:5]
    assert "sleepy" in sorted(seeds)[5:]

#output filters start here

@pytest.fixture(scope="function")
def sentences():
    sentences_ = ["""red coat myself very unwell this morning that has \
    passed off much better of me if I speak plainer ?""",
    'red coat myself very unwell this morning that if it is .',
    'red coat myself very unwell this morning and pack her trunk afresh .',
    """red coat myself very unwell this morning that has passed off pleasantly \
    to the following morning every hope of an illiterate and miserly father and mother .""",
    'red coat myself very well madam said .',
    'red coat myself very well together .',
    'red coat myself very unwell this morning .',
    'red coat myself very well for the first two months .',
    'red coat myself very well that .',
    """red coat myself very unwell this morning that if he comes\
    into the regulars and among his former indolence ."""]
    return sentences_


def test_length(sentences):
    reduced_sentences = output_filters.filter_length(sentences, wordcount=5)
    for sentence in reduced_sentences:
        assert len(sentence.split()) < 6


def test_length_null(sentences):
    reduced_sentences = output_filters.filter_length(sentences)
    same_sentences = output_filters.filter_length(reduced_sentences)
    assert len(same_sentences) == len(reduced_sentences)


def test_filter_pos(sentences):
    reduced_sentences = output_filters.filter_pos(sentences)
    content_word_tags = ['VB', 'NN', 'JJ']
    for sentence in reduced_sentences:
        has_content_word = False
        for word, tag in pos_tag(sentence):
            if tag in content_word_tags:
                has_content_word = True
        assert has_content_word is True


def test_filter_NN_VV(sentences):
    reduced_sentences = output_filters.filter_NN_VV(sentences)
    for sentence in reduced_sentences:
        has_NN = False
        is_valid = False
        for word, tag in pos_tag(sentence):
            if tag[:2] == "NN":
                has_NN = True
            if has_NN and tag[:2] == "VB":
                is_valid = True
        assert is_valid is True



