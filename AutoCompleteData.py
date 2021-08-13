class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int

    def __init__(self, completed_sentence: str, source_text: str, offset: int, score: int):
        """
        save data about the completed sentence
        :param completed_sentence: the complete sentence
        :param source_text: the source file of the sentence
        :param offset: the row number of the line in the file
        :param score: the score of the completion
        """
        self.completed_sentence = completed_sentence.strip()
        self.source_text = source_text
        self.offset = offset
        self.score = score

    def __str__(self):
        return f" {self.completed_sentence}  ({self.source_text} {self.offset}) score: {self.score}"
