from GlobalFunctions import clean_sentence


class WordDB:
    """
    this class uses for: 1. save all the word in the text files
                        2. for every word save all the words with missed characters
    In order to correct the mistakes by this information
    """

    def __init__(self):
        self.__words_missing_char = {}

    def add_line(self, line):
        """
        add line of text to the data
        :param line: line to add to the data
        """
        line = clean_sentence(line).split()
        for word in line:
            self.add_word(word)

    def add_word(self, word):
        """
        for every word- add the word to the all_word dictionary
        and add the word without one char- for example: for the word: hello
        we add the words: ello hllo helo hell and match them to the original word: hello
        and define for every word in each index the letter missing
        :param word: the word to add
        """
        for i in range(len(word)):
            word_without_char = word[:i] + word[i + 1:]
            if self.__words_missing_char.get(word_without_char) is None:
                self.__words_missing_char[word_without_char] = {i: [word]}
            else:
                if self.__words_missing_char[word_without_char].get(i) is None:
                    self.__words_missing_char[word_without_char][i] = [word]
                else:
                    if word not in self.__words_missing_char[word_without_char].get(i):
                        self.__words_missing_char[word_without_char].get(i).append(word)

    def get_word_with_index(self, word, index):
        """
        get word and index in the word and return all the words that have a additional char in this index
        :param word: word to search
        :param index: index of the added char
        :return: the array of words
        """
        if self.__words_missing_char.get(word) is None:
            return None
        array = self.__words_missing_char[word].get(index)
        if array is None:
            return None
        return array
