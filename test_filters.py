import pytest
import input_filters
import output_filters
import chatbot_brain
import random
from nltk.tokenize import wordpunct_tokenize
from nltk import pos_tag

"""Tests of the brain start here. File contains tests of the input filters
then the output filters at the end. """


@pytest.fixture(scope="session")
def _bot_brain():
    bot = chatbot_brain.Chatbot()
    bot.load_lexicons()
    return bot, bot.word_pos, bot.bi_lexicon

random.seed(0)

stock = u"What a funny thing to say!"

sentences_ = [
    "red coat myself very unwell this morning that has \
    passed off much better of me if I speak plainer ?",
    "red coat myself very unwell this morning that if it is .",
    "red coat myself very unwell this morning and pack her trunk afresh.",
    "red coat myself very unwell this morning that has passed off pleasantly \
    to the following morning every hope of an illiterate and miserly father \
    and mother .""",
    "red coat myself very well madam said.",
    "red coat myself very well together.",
    "red coat myself very unwell this morning.",
    "red coat myself very well for the first two months.",
    "red coat myself very well that.",
    "red coat myself very unwell this morning that if he comes\
    into the regulars and among his former indolence."
    ]

short_sentences = [
    "".join(sent) for sent in sentences_ if len(sent.split()) <= 8
    ]


def test_initialize_bot():
    u"""Assert instantiated chatbot is a Chatbot."""
    bot = chatbot_brain.Chatbot()
    assert isinstance(bot, chatbot_brain.Chatbot)


def test_fill_lexicon(_bot_brain):
    u"""Assert training adds key, value pairs to both lexicons."""
    bot, pos, lex = _bot_brain
    assert len(bot.tri_lexicon) > 0
    assert len(bot.bi_lexicon) > 0


def test_compose_response(_bot_brain):
    u"""Assert Chatbot is untrained when instantiated."""
    bot, pos, lex = _bot_brain
    filters = ["Length Filter", "No Filter Selected"]
    output, sausage = bot.compose_response(
        input_sent="How are you doing?",
        input_key="No Filter Selected",
        output_filter=filters,
        brain="Bigram Brain")
    assert "," not in output[0]
    for sentence in output:
        assert "." not in sentence[:-1]


def test_i_filter_random_empty_words(_bot_brain):
    u"""Assert an empty string is not found in the default lexicon."""
    bot, pos, lex = _bot_brain
    words = [""]
    assert bot.i_filter_random(words) == stock


def test_i_filter_random_words_not_in_lexicon(_bot_brain):
    u"""Assert if all words are not in lexicon the default is returned."""
    bot, pos, lex = _bot_brain
    words = ["moose", "bear", "eagle"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot.i_filter_random(words) == stock


def test_i_filter_random_words_in_lexicon(_bot_brain):
    u"""Assert if all words are in lexicon, a word is returned."""
    bot, pos, lex = _bot_brain
    words = ["car", "boat", "train"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot.i_filter_random(words) in lex


def test_i_filter_random_one_word_in_lexicon(_bot_brain):
    u"""Assert if one word is in lexicon that word is returned."""
    bot, pos, lex = _bot_brain
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot.i_filter_random(words) == "car"


def test_o_filter_random(_bot_brain):
    u"""Assert the returned element is in the initial list."""
    bot, pos, lex = _bot_brain
    assert bot.o_filter_random(sentences_) in sentences_


def test_pair_seeds_one_possible_pair(_bot_brain):
    u"""Assert if only one word is in the lexicon it and its pair returned."""
    bot, pos, lex = _bot_brain
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot._pair_seed(words[0]) == ["car", "benz"]


def test_pair_seeds_all_possible_pairs(_bot_brain):
    u"""Assert if all words are in the lexicon the seed's pair is returned."""
    bot, pos, lex = _bot_brain
    words = ["car", "boat", "train"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    for word in words:
        assert bot._pair_seed(word) == [word, bot.bi_lexicon[word][0]]


def test_pair_seeds_one_possible_pair_due_to_punct(_bot_brain):
    u"""Assert only strings without stop characters are returned."""
    bot, pos, lex = _bot_brain
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {
        "car": [".", "!", "benz"],
        "boat": ["sail"],
        "train": ["track"]
        }
    assert bot._pair_seed(words[0]) == ["car", "benz"]


def test_filter_recursive_stops(_bot_brain):
    u"""Assert recursion stops when base case is reached."""
    filters = []
    bot, pos, lex = _bot_brain
    strings, output_dict = bot._filter_recursive(sentences_, filters)
    assert strings == sentences_
    assert output_dict == {}


def test_filter_recursive_one_recursive_call(_bot_brain):
    u"""Assert expected filtering occurs after one recursive call."""
    filters = [output_filters.funct_dict["Length Filter"]]
    bot, pos, lex = _bot_brain
    strings, output_dict = bot._filter_recursive(sentences_, filters)
    print "Strings: {}".format(strings)
    print "Short_sentences: {}".format(short_sentences)
    assert strings == short_sentences
    assert output_dict == {filters[0].__name__: short_sentences}


def test_filter_recursive_two_recursive_calls(_bot_brain):
    u"""Assert expected filtering occurs after two recursive calls."""
    filters = [
        output_filters.funct_dict["Length Filter"],
        output_filters.funct_dict["No Filter Selected"]
        ]
    bot, pos, lex = _bot_brain
    strings, output_dict = bot._filter_recursive(sentences_, filters)
    print "Strings: {}".format(strings)
    print "Short_sentences: {}".format(short_sentences)
    assert strings == short_sentences
    assert output_dict == {
        filters[0].__name__: short_sentences,
        filters[1].__name__: short_sentences
        }
    pass






u"""Input filter tests begin here"""









def test_small_talk_filter(_bot_brain):
    bot, pos, lex = _bot_brain
    tester = wordpunct_tokenize("raining snowing sunny weather")
    weather_opts = ["Talking about the weather is such a bore.",
        "I'm not the weatherman!"]
    sentence = input_filters.filter_small_talk(tester, lex)
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


def test_length(sentences, _bot_brain):
    bot, pos, lex = _bot_brain
    reduced_sentences = output_filters.filter_length(sentences, pos)
    for sentence in reduced_sentences:
        assert len(sentence.split()) <= 8


def test_length_null(sentences, _bot_brain):
    bot, pos, lex = _bot_brain
    reduced_sentences = output_filters.filter_length(sentences, pos)
    same_sentences = output_filters.filter_length(reduced_sentences, pos)
    assert len(same_sentences) == len(reduced_sentences)


def test_filter_pos(sentences, _bot_brain):
    bot, pos, lex = _bot_brain
    reduced_sentences = output_filters.filter_pos(sentences, pos)
    content_word_tags = ['VB', 'NN', 'JJ']
    for sentence in reduced_sentences:
        has_content_word = False
        for word, tag in pos_tag(sentence):
            if tag in content_word_tags:
                has_content_word = True
        assert has_content_word is True


def test_filter_NN_VV(sentences, _bot_brain):
    bot, pos, lex = _bot_brain
    reduced_sentences = output_filters.filter_NN_VV(sentences, pos)
    for sentence in reduced_sentences:
        has_NN = False
        is_valid = False
        for word, tag in pos_tag(sentence):
            if tag[:2] == "NN":
                has_NN = True
            if has_NN and tag[:2] == "VB":
                is_valid = True
        assert is_valid is True
