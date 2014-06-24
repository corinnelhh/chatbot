import output_filters

sentences = ["good breeding and of the match Lady Catherine is not know and let us the express To morrow fortnight and by any thing in a month You see it and sometimes made the very gravely glancing.",
            "here are to the company I congratulate you have seen Collins and he had recommended him from Jane I dare say",
            "hello my friend I hope you are well",
            "good evening gracious lady you are most considerate",
            "may I entertain you with a list of seasonal chocolates",
            "perhaps your kindness shall be rewarded"]



def test_length():
    reduced_sentences = output_filters.filter_length(sentences)
    assert len(reduced_sentences) == 4
