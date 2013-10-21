DELIMITER = '|'


class Data:
    def __init__(self, data, configuration={}):
        self.__configuration = configuration
        self.__delimiter = self.__configuration.get('delimiter', DELIMITER)
        self.__data = data

    def getRecords(self):
        return (Record(record, self.__delimiter) for record in self.__data)


class Record:
    def __init__(self, data, delimiter=DELIMITER):
        self.__data = data
        self.__delimiter = delimiter

    def getFields(self):
        return self.__data.split(self.__delimiter)