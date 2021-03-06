DELIMITER = '|'


class Data:
    def __init__(self, data, configuration=None):
        if not configuration:
            configuration = {}
        self.__configuration = configuration
        self.__records = [Record(record, configuration) for record in data]

    def get_records(self):
        return self.__records


class Record:
    def __init__(self, data, configuration):
        self.__expected_size = configuration.get('size', 0)
        self.__delimiter = configuration.get('delimiter', DELIMITER)
        columns = configuration.get('columns', [])

        def get_meta(index):
            return columns[index] if len(columns) > index else {}

        self.__fields = [Field(value, index, get_meta(index)) for index, value in enumerate(data.split(self.__delimiter))]

    def get_fields(self):
        return self.__fields

    def get_field(self, index):
        if index < 0 or index >= len(self.__fields):
            raise IndexError()
        return self.__fields[index]

    def get_expected_size(self):
        return self.__expected_size

    def __str__(self):
        return self.__delimiter.join([str(field) for field in self.get_fields()])


class Field:
    def __init__(self, value, index, meta):
        self.__value = value
        self.__meta = meta
        self.__index = index

    def get_value(self):
        return self.__value

    def get_meta(self):
        return self.__meta

    def get_name(self):
        return self.__meta.get('name', '<Field #%s>' % self.__index)

    def __str__(self):
        return self.get_value()
