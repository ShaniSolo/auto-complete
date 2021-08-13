from GlobalFunctions import clean_sentence

from TrieNode import TrieNode


class SuffixTrie:
    def __init__(self):
        self.__root = TrieNode()

    def add_line(self, line, line_id):
        """
        add line to the suffix trie: add all the suffix of the line to the trie
        :param line: line to add
        :param line_id: the line id
        """
        line = clean_sentence(line)
        for i in range(len(line)):
            self.add_word(line[i:], line_id)

    def add_word(self, line, line_id):
        """
        add string to the suffix trie
        :param line: the string to add
        :param line_id: the line id
        """
        node = self.__root
        for char in line:
            if node.get_next_node(char) is None:
                node_to_add = TrieNode()
                node.add_node(char, node_to_add)
            node.add_line(line_id)
            node = node.get_next_node(char)
        node.add_line(line_id)
        node_to_add = TrieNode()
        node.add_node("$", node_to_add)
        node = node.get_next_node("$")
        node.add_line(line_id)

    def search_sentence(self, sentence):
        """
        get sentence and search it in the suffix trie
        :param sentence: the sentence to add
        :return: Return the line number that this sentence is in
        """
        node = self.__root
        sentence = clean_sentence(sentence)
        i = 0
        while i < len(sentence):
            node = node.get_next_node(sentence[i])
            if node is None:
                return []
            i += 1
        return node.get_lines()
