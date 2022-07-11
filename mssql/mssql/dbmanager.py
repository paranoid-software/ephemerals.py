import abc
from abc import ABC

import pyodbc


class DbManagerProtocol(ABC):
    @abc.abstractmethod
    def create_database(self, name: str):
        pass

    @abc.abstractmethod
    def execute_non_query(self, sentence: str, at: str):
        pass

    @abc.abstractmethod
    def execute_query(self, sentence: str, at: str) -> [dict]:
        pass

    @abc.abstractmethod
    def drop_database(self, name: str):
        pass


class DbManager(DbManagerProtocol):

    __server_connection_string: str

    def __init__(self, server_connection_string):
        self.__server_connection_string = server_connection_string

    def create_database(self, name: str):
        cnn = self.__get_connection(auto_commit=True)
        cursor = cnn.cursor()
        cursor.execute(f'CREATE DATABASE {name};')
        cursor.close()
        cnn.close()

    def execute_non_query(self, sentence: str, at: str):
        cnn = self.__get_connection(at)
        cursor = cnn.cursor()
        cursor.execute(sentence)
        cnn.commit()
        cursor.close()
        cnn.close()

    def execute_query(self, sentence: str, at: str) -> [dict]:
        cnn = self.__get_connection(at)
        cursor = cnn.cursor()
        cursor.execute(sentence)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        cursor.close()
        cnn.close()
        return results

    def drop_database(self, name: str):
        cnn = self.__get_connection(auto_commit=True)
        cursor = cnn.cursor()
        cursor.execute(f'DROP DATABASE {name};')
        cursor.close()
        cnn.close()

    def __get_connection(self, db_name=None, auto_commit=False):
        db_connection_string = None
        if db_name is not None:
            db_connection_string = f'{self.__server_connection_string};DATABASE={db_name};'
        return pyodbc.connect(db_connection_string or self.__server_connection_string, autocommit=auto_commit)
