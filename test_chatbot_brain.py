import pytest

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


def test_create_chains():
    bot = chatbot_brain.Chatbot()
    output = bot.generate_response("How are you doing?")
    assert "," not in output[0]
