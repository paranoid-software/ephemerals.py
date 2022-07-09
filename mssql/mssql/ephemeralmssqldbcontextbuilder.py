from typing import List

from mssql import EphemeralMsSqlDbContext, DbManagerProtocol


class EphemeralMsSqlDbContextBuilder:

    __scripts: List[str]

    def __init__(self):
        self.__scripts = []

    def add_script_from_file(self, filepath):
        file = open(filepath)
        file_content = file.read()
        self.__scripts.append(file_content)
        return self

    def add_script(self, sentence):
        self.__scripts.append(sentence)
        return self

    def build(self,
              connection_string,
              db_manager: DbManagerProtocol = None):
        return EphemeralMsSqlDbContext(connection_string,
                                       self.__scripts,
                                       db_manager)
