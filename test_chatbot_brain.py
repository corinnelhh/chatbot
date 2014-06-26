import chatbot_brain
import random
import output_filters

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


def test_initialize_bot_is_untrained():
    u"""Assert Chatbot is untrained when instantiated."""
    bot = chatbot_brain.Chatbot()
    assert len(bot.tri_lexicon) == 0
    assert len(bot.bi_lexicon) == 0


def test_fill_lexicon():
    u"""Assert training adds key, value pairs to both lexicons."""
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    assert len(bot.tri_lexicon) > 0
    assert len(bot.bi_lexicon) > 0


def test_compose_response():
    u"""Assert Chatbot is untrained when instantiated."""
    bot = chatbot_brain.Chatbot()
    output, sausage = bot.compose_response(input_sent="How are you doing?")
    assert "," not in output[0]
    for sentence in output:
        assert "." not in sentence[:-1]


def test_i_filter_random_empty_words():
    u"""Assert an empty string is not found in the default lexicon."""
    bot = chatbot_brain.Chatbot()
    words = [""]
    assert bot.i_filter_random(words) == stock


def test_i_filter_random_words_not_in_lexicon():
    u"""Assert if all words are not in lexicon the default is returned."""
    bot = chatbot_brain.Chatbot()
    words = ["moose", "bear", "eagle"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot.i_filter_random(words) == stock


def test_i_filter_random_words_in_lexicon():
    u"""Assert if all words are in lexicon, a word is returned."""
    bot = chatbot_brain.Chatbot()
    words = ["car", "boat", "train"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot.i_filter_random(words) in bot.bi_lexicon


def test_i_filter_random_one_word_in_lexicon():
    u"""Assert if one word is in lexicon that word is returned."""
    bot = chatbot_brain.Chatbot()
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot.i_filter_random(words) == "car"


def test_o_filter_random():
    u"""Assert the returned element is in the initial list."""
    bot = chatbot_brain.Chatbot()
    assert bot.o_filter_random(sentences_) in sentences_


def test_pair_seeds_one_possible_pair():
    u"""Assert if only one word is in the lexicon it and its pair returned."""
    bot = chatbot_brain.Chatbot()
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    assert bot._pair_seed(words[0]) == ["car", "benz"]


def test_pair_seeds_all_possible_pairs():
    u"""Assert if all words are in the lexicon the seed's pair is returned."""
    bot = chatbot_brain.Chatbot()
    words = ["car", "boat", "train"]
    bot.bi_lexicon = {"car": ["benz"], "boat": ["sail"], "train": ["track"]}
    for word in words:
        assert bot._pair_seed(word) == [word, bot.bi_lexicon[word][0]]


def test_pair_seeds_one_possible_pair_due_to_punct():
    u"""Assert only strings without stop characters are returned."""
    bot = chatbot_brain.Chatbot()
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {
        "car": [".", "!", "benz"],
        "boat": ["sail"],
        "train": ["track"]
        }
    assert bot._pair_seed(words[0]) == ["car", "benz"]


def test_filter_recursive_stops():
    u"""Assert recursion stops when base case is reached."""
    filters = []
    bot = chatbot_brain.Chatbot()
    strings, output_dict = bot._filter_recursive(sentences_, filters)
    assert strings == sentences_
    assert output_dict == {}


def test_filter_recursive_one_recursive_call():
    u"""Assert expected filtering occurs after one recursive call."""
    filters = [output_filters.funct_dict["Length Filter"]]
    bot = chatbot_brain.Chatbot()
    strings, output_dict = bot._filter_recursive(sentences_, filters)
    print "Strings: {}".format(strings)
    print "Short_sentences: {}".format(short_sentences)
    assert strings == short_sentences
    assert output_dict == {filters[0].__name__: short_sentences}


    # def _filter_recursive(self, strings, filters, output_dict={}):
    #     u"""Return list of strings or call the next filter function."""
    #     if filters == []:
    #         return strings, output_dict
    #     else:
    #         output_dict[filters[0].__name__] = filters[0](strings)
    #         return self._filter_recursive(
    #             filters[0](strings),
    #             filters[1:],
    #             output_dict
    #             )


# untested methods:
# _create_chains
# _chain_filters
# _filter_recursive
# _make_sausage