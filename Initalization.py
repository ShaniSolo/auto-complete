import os
from SuffixTrie import SuffixTrie
from LinesDB import LinesDB
from WordDB import WordDB
from SourceFilesDB import SourceDB


def initialize():
    """
    read every file in the directory, and add each row to the linesDB, suffixTrie and wordDB
    :return: the suffix trie, linesDB, wordDB
    """
    suffixTrie = SuffixTrie()
    lines_DB = LinesDB()
    word_DB = WordDB()
    source_DB = SourceDB()

    print("Loading the files and preparing the system...")
    for pack in os.walk("./2021-archive/python-3.8.4-docs-text/installing"):
        for f in pack[2]:
            file_path = pack[0] + "\\" + f
            with open(file_path, "r", encoding="utf8") as file:
                lines = file.readlines()
                src_id = source_DB.add_source(file_path)
                for i in range(len(lines)):
                    id = lines_DB.add_line(src_id, i)
                    suffixTrie.add_line(lines[i], id)
                    word_DB.add_line(lines[i])
    return suffixTrie, lines_DB, word_DB
