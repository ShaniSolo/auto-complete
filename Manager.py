from Initalization import initialize
from AutoComplete import AutoComplete


class Manager:

    def __init__(self):
        """
        initalize the system
        """
        self.__suffix_trie, self.__linesDB, self.__wordsDB = initialize()
        self.__auto_complete = AutoComplete(self.__suffix_trie, self.__linesDB, self.__wordsDB)

    def run(self):
        """
        get input from the user and search the sentences
        """
        print("The system is ready. Enter your text:")
        while True:
            sentence = ""
            add_to_sentence = input()
            while add_to_sentence != "#":
                sentence += add_to_sentence
                out = self.__auto_complete.get_best_k_completions(sentence)
                print(f"Here are {len(out)} suggestion :")
                for i in range(len(out)):
                    print(f"{i + 1}. " + str(out[i]))
                add_to_sentence = input(sentence)
            print("Enter your text")
