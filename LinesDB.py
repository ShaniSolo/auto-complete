from SourceFilesDB import SourceDB
import linecache


class LinesDB:
    _instance = None
    _was_init = False

    def __new__(cls, *args, **kwargs):
        if not LinesDB._instance:
            LinesDB._instance = object.__new__(cls)
        return LinesDB._instance

    def __init__(self):
        """
        match id to every line in the text files
        """
        if not LinesDB._was_init:
            self.__lines_ids = 0
            self.__lines_array = []
            self.__src_DB = SourceDB()

    def add_line(self, src, position):
        """
        add new line to the DB
        :param src: the source file name
        :param position: the line number in the file
        :return: the ID of the new line
        """

        self.__lines_array.append((src, position))
        line = self.__lines_ids
        self.__lines_ids += 1
        return line

    def get_lines(self, lines_ids):
        """
        get array of lines ID and return the lines that match to the ids
        :param lines_ids: array of ids
        :return: lines
        """
        lines_by_id = []
        for i in lines_ids:
            src = self.__src_DB.get_source(self.__lines_array[i][0])
            line = linecache.getline(src, self.__lines_array[i][1]+1)
            lines_by_id.append((line, src, self.__lines_array[i][1]))
        return lines_by_id
