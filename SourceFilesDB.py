class SourceDB:
    _instance = None
    _was_init = False

    def __new__(cls, *args, **kwargs):
        if not SourceDB._instance:
            SourceDB._instance = object.__new__(cls)
        return SourceDB._instance

    def __init__(self):
        """
        match id to every line in the text files
        """
        if not SourceDB._was_init:
            self.__sources_ids = 0
            self.__source_array = []

    def add_source(self, src):
        """
        add new line to the DB
        :param src: the source file name
        :param position: the line number in the file
        :return: the ID of the new line
        """
        id = self.__sources_ids
        self.__source_array.append(src)
        self.__sources_ids += 1
        return id

    def get_source(self, source_id):
        """
        get array of lines ID and return the lines that match to the ids
        :param lines_ids: array of ids
        :return: lines
        """
        return self.__source_array[source_id]
