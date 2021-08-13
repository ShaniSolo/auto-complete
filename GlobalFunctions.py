from string import ascii_lowercase


def clean_sentence(sentence):
    """
    convert the sentence to clean sentence- lower case and without special chars
    :param sentence: sentence to clean
    :return: clean sentence
    """
    words = sentence.lower().split()
    clean_sent = ""
    for word in words:
        clean_sent += (''.join(list(map(lambda x: x if x in ascii_lowercase or x in "1234567890" else '', list(word))))) + " "
    return clean_sent[:-1]
