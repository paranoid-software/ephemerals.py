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
    def get_all_database_names(self) -> [str]:
        pass

    @abc.abstractmethod
    def get_all_table_names(self, at: str) -> [str]:
        pass

    @abc.abstractmethod
    def get_row_count(self, at: str, table_name) -> [str]:
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

    def get_all_database_names(self) -> [str]:
        cnn = self.__get_connection()
        cursor = cnn.cursor()
        cursor.execute('SELECT name FROM master.sys.databases;')
        db_names = []
        for row in cursor.fetchall():
            db_names.append(row[0])
        cursor.close()
        cnn.close()
        return db_names

    def get_all_table_names(self, at: str) -> [str]:
        cnn = self.__get_connection(at)
        cursor = cnn.cursor()
        table_names = []
        for row in cursor.tables():
            table_names.append(row.table_name)
        cursor.close()
        cnn.close()
        return table_names

    def get_row_count(self, at: str, table_name) -> [str]:
        cnn = self.__get_connection(at, True)
        cursor = cnn.cursor()
        cursor.execute(f'SELECT count(*) FROM {table_name} with(nolock);')
        row_count = cursor.fetchone()[0]
        cursor.close()
        cnn.close()
        return row_count

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
