import chatbot_brain

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


def test_initialize_bot():
    bot = chatbot_brain.Chatbot()
    assert len(bot.tri_lexicon) == 0
    assert len(bot.bi_lexicon) == 0


def test_fill_lexicon():
    bot = chatbot_brain.Chatbot()
    bot.fill_lexicon()
    assert len(bot.tri_lexicon) > 0
    assert len(bot.bi_lexicon) > 0


def test_compose_response():
    bot = chatbot_brain.Chatbot()
    output = bot.compose_response(input_sent="How are you doing?")
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
    bot.bi_lexicon = {"car": "mercedes", "boat": "sail", "train": "track"}
    assert bot.i_filter_random(words) == stock


def test_i_filter_random_words_in_lexicon():
    u"""Assert if all words are in lexicon, a word is returned."""
    bot = chatbot_brain.Chatbot()
    words = ["car", "boat", "train"]
    bot.bi_lexicon = {"car": "mercedes", "boat": "sail", "train": "track"}
    assert bot.i_filter_random(words) in bot.bi_lexicon


def test_i_filter_random_one_word_in_lexicon():
    u"""Assert if one word is in lexicon that word is returned"""
    bot = chatbot_brain.Chatbot()
    words = ["car", "bear", "eagle"]
    bot.bi_lexicon = {"car": "mercedes", "boat": "sail", "train": "track"}
    assert bot.i_filter_random(words) == "car"


def test_o_filter_random():
    u"""Assert the returned element is in the initial list."""


        def o_filter_random(self, sentences):
        u"""Return randomly selected sentence from sentecnces"""
        return random.choice(sentences)

# untested methods:
# o_filter_random
# _create_chains
# _pair_seed
# _chain_filters
# _filter_recursive
