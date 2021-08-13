from GlobalFunctions import clean_sentence
from AutoCompleteData import AutoCompleteData


class AutoComplete:
    def __init__(self, suffix_trie, linesDB, wordsDB):
        """
        manage the search matching from data, by the score of the result
        :param suffix_trie: DB structer (singleton) for scanning input
        :param linesDB: DB structer (singleton) for lines data
        :param wordsDB: DB structer (singleton) for saving all words
        """
        self.__suffix_trie = suffix_trie
        self.__linesDB = linesDB
        self.__wordsDB = wordsDB
        self.__found_lines_dict = {}

    def get_best_k_completions(self, prefix: str):
        """
        find the best 5 result for the user's input
        :param prefix: the input from the user
        :return:the most equal five results
        """
        result = self.manage_search(prefix)
        result.sort(key=lambda res: (-res.score, res.completed_sentence.lower()))
        return result[:5]

    def search_word(self, array_words, index):
        """
        find the index of char in array of word, by his index in the sentence of that words
        :param array_words: array fo the sentence words
        :param index: the index of the char in the sentence
        :return: the index of the word in the array, and the index of the char in the word
        """
        count = 0
        for i in range(len(array_words)):
            if count + len(array_words[i]) + 1 < index:
                count += len(array_words[i]) + 1
            else:
                return i, index - count
        return -1

    def exactly(self, sentence):
        """
        find all the exact matching
        :param sentence: string to search
        :return: lines in which the string is located
        """
        score = 2 * len(sentence)
        lines = self.__suffix_trie.search_sentence(sentence)
        lines = self.__linesDB.get_lines(lines)
        lines_full_data = []
        for line in lines:
            if self.__found_lines_dict.get(line) is None:
                self.__found_lines_dict[line] = 0
                lines_full_data.append(AutoCompleteData(line[0], line[1], line[2], score))

        return lines_full_data

    def replace(self, sentence, index):
        """
         find all the matching with one replace, in the given index
        :param sentence:the original sentence
        :param index:the index of the char to replace
        :return: lines in which the string with the replace is located
        """
        score = 2 * len(sentence) - 2
        result_to_return = []
        if sentence[index] == " ":
            sentence = sentence[:index] + sentence[index + 1:]
            index -= 1
        words_array = sentence.split()
        index_in_array = self.search_word(words_array, index)
        if index_in_array == -1:
            return []
        word_to_replace = words_array[index_in_array[0]][:index_in_array[1]] + words_array[index_in_array[0]][
                                                                               index_in_array[1] + 1:]
        all_replaced_words = self.__wordsDB.get_word_with_index(word_to_replace, index_in_array[1])
        if all_replaced_words is None:
            return []
        for word in all_replaced_words:
            words_array[index_in_array[0]] = word
            new_sentence_to_search = " ".join(words_array)
            lines = self.__suffix_trie.search_sentence(new_sentence_to_search)
            lines = self.__linesDB.get_lines(lines)
            for line in lines:
                linescore = score - (12 - 2 * index) if index < 5 else score - 2
                if self.__found_lines_dict.get(line) is None:
                    self.__found_lines_dict[line] = 0
                    result_to_return.append(AutoCompleteData(line[0], line[1], line[2], linescore))
            return result_to_return

    def add(self, sentence, index):
        """
         find all the matching with one remove char, in the given index
        :param sentence:the original sentence
        :param index:the index of the char to remove
        :return: lines in which the string without the char in the given index is located
        """
        score = 2 * len(sentence) - 2
        result_to_return = []
        words_array = sentence.split()
        index_in_array = self.search_word(words_array, index)
        if index_in_array == -1:
            return []
        all_added_words = self.__wordsDB.get_word_with_index(words_array[index_in_array[0]], index_in_array[1])
        if all_added_words is None:
            return []
        for word in all_added_words:
            words_array[index_in_array[0]] = word
            new_sentence_to_search = " ".join(words_array)
            lines = self.__suffix_trie.search_sentence(new_sentence_to_search)
            lines = self.__linesDB.get_lines(lines)
            for line in lines:
                linescore = score - (6 - index) if index < 5 else score - 1
                if self.__found_lines_dict.get(line) is None:
                    self.__found_lines_dict[line] = 0
                    result_to_return.append(AutoCompleteData(line[0], line[1], line[2], linescore))
            return result_to_return

    def delete(self, sentence, index):
        """
         find all the matching with add one char, in the given index
        :param sentence:the original sentence
        :param index:the index to add the char
        :return: lines in which the string with a new char in the given index is located
        """
        words = sentence.split()
        score = 2 * len(sentence)
        res = self.search_word(words, index)
        result_to_return = []
        if res != -1:
            removed = words[res[0]][:res[1]] + words[res[0]][res[1] + 1:]
            if self.__suffix_trie.search_sentence(removed):
                tmp_words = words
                tmp_words[res[0]] = removed
                tmp_sentence = ' '.join(tmp_words)
                lines = self.__suffix_trie.search_sentence(tmp_sentence)
                lines = self.__linesDB.get_lines(lines)
                for line in lines:
                    linescore = score - (12 - 2 * index) if index < 5 else score - 2
                    if self.__found_lines_dict.get(line) is None:
                        self.__found_lines_dict[line] = 0
                        result_to_return.append(AutoCompleteData(line[0], line[1], line[2], linescore))
                return result_to_return
        return []

    def correct_word(self, sentence, index, func):
        """
        send the given word to the givw func for each index
        :param sentence: the original sentence
        :param index: the index to start the checking- using in the score
        :param func: the func to send to
        :return: the lines returned from the func
        """
        ans = []
        start_index = index
        if index >= len(sentence):
            return []
        if index < 4:
            end_index = index + 1
        else:
            end_index = len(sentence)
        for i in range(start_index, end_index):
            ans += func(sentence, i)
        return ans

    def manage_search(self, sentence):
        """
        manage the searching matching completes by the score
        :param sentence: the original sentence
        :return:all the matching lines with the highest score, at least five result (or, if there is no, five, all the results)
        """
        sentence = clean_sentence(sentence)
        k = 5
        funcs = [self.replace, self.delete, self.add]
        func_index = [[2], [0], [0, 1, 2], [0], [0, 1, 2], [0], [1, 2], [1, 2], [1]]
        index = [[4], [4], [3, 4, 3], [2], [1, 2, 3], [0], [2, 1], [1, 0], [0]]
        auto_complete = []
        i = 0
        auto_complete += self.exactly(sentence)
        k -= len(auto_complete)
        while k > 0 and i < len(index):
            res = []
            for j in range(len(index[i])):
                res += self.correct_word(sentence, index[i][j], funcs[func_index[i][j]])
            k -= len(res)
            auto_complete += res
            i += 1
        self.__found_lines_dict = {}
        return auto_complete
