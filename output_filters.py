def filter_length(sentences, wordcount=13):
    """Takes in a list of sentences and returns a reduced list,

    that contains only sentences with less than <wordcount> words."""

    for sentence in sentences[:]:
        if len(sentence.split())>13:
            sentences.remove(sentence)
    return sentences
