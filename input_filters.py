def i_filter_small_talk(dict_key, keyword=None):
    """
    Takes in a dictkey and an optional keyword. Sentences are randomly
    selected from the list of values. If a keyword is present,
    keyword is added into the output string.
    """

    small_talk_dict = {'unknown_word' : ["What a funny thing to say!",
        "That's a new one!", "Huh!"],'weather' :
        ["Talking about the weather is such a bore.",
        "I'm not the weatherman!"], 'feelings' : ["Why do you care how I feel?",
        "More importantly, how do you feel?", "Really, are *you* {}".format()],
        'sports' : ["You're a sports fan!", "I've never been much of an athlete..."]
    }

    if 
