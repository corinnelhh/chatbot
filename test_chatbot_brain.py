import pytest

import chatbot_brain

def test_initialize_bot():
    bot = Chatbot()
    assert len(bot.tri_lexicon) == 0
    assert len(bot.bi_lexicon) == 0

def test_fill_lexicon():
    bot = Chatbot()
    bot.fill_lexicon()
    assert len(bot.tri_lexicon) > 0
    assert len(bot.bi_lexicon) > 0


def test_create_chains():
    bot = Chatbot()
    output = bot.create_chains()
    assert "," not in output[0]
