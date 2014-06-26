import chatbot_brain


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
    u"""Assert the returned word is in the lexicon and is not a stop char."""
    bot = chatbot_brain.Chatbot()
    words = [""]
    assert bot.i_filter_random(words) == u"What a funny thing to say!"

# untested methods:
# i_filter_random
# o_filter_random
# _create_chains
# _pair_seed
# _chain_filters
# _filter_recursive
