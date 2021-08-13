class TrieNode:
    match_chars = "abcdefghijklmnopqrstuvwxyz $1234567890"

    def __init__(self, array_lines=None):
        """
        represent node in the suffixTrie, contain dictionary for every char and the lines ID
        :param array_lines:
        """
        if array_lines is None:
            array_lines = []
        self.__array_lines = array_lines
        self.__chars_array = [None for i in range(38)]

    def add_node(self, char, node):
        """
        get char and node and add the node to the array in the index of the char
        :param char: the char to add
        :param node: node to add
        """
        self.__chars_array[TrieNode.match_chars.index(char)] = node

    def add_line(self, line):
        """
        add line to the lines array- the mean is that this string exist in this line
        :param line: line to add
        """
        if line not in self.__array_lines:
            self.__array_lines.append(line)

    def get_lines(self):
        """
        get the lines array
        :return: the lines array
        """
        return self.__array_lines

    def get_next_node(self, char):
        """
        get char and return the node in the char index array
        :param char:
        :return:
        """
        return self.__chars_array[TrieNode.match_chars.index(char)]
