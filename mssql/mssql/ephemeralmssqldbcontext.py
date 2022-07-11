import uuid

from mssql import DbManagerProtocol, DbManager


class EphemeralMsSqlDbContext:

    __db_manager: DbManagerProtocol
    __scripts: [str]
    __db_name: str

    def __init__(self,
                 connection_string,
                 scripts: [str],
                 db_manager: DbManagerProtocol = None):

        supported_data_sources = ['localhost', '127.0.0.1']

        if self.__get_connection_string_params(connection_string).get('SERVER', None) not in supported_data_sources:
            raise Exception('Ephemeral database server must be local, use localhost or 127.0.0.1 as server address.')

        if 'DATABASE' in connection_string:
            raise Exception('Ephemeral database name should not be included on the connection string, please remove DATABASE parameter.')

        self.__db_manager = db_manager or DbManager(connection_string)
        self.__scripts = scripts

    def __enter__(self):
        self.__db_name = f'edb_{uuid.uuid4().hex}'
        self.__db_manager.create_database(self.__db_name)
        for script in self.__scripts:
            self.__db_manager.execute_non_query(script, self.__db_name)
        return self, self.__db_name

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__db_manager.drop_database(self.__db_name)

    def get_all_database_names(self):
        query_result = self.__db_manager.execute_query(
            'SELECT name FROM sys.databases;',
            'master'
        )
        return [item.get('name') for item in query_result]

    def get_all_table_names(self):
        query_result = self.__db_manager.execute_query(
            f'SELECT name FROM sys.tables;',
            self.__db_name
        )
        return [item.get('name') for item in query_result]

    def get_row_count(self, table_name) -> int:
        query_result = self.__db_manager.execute_query(
            f'SELECT count(*) as row_count FROM {table_name} WITH(NOLOCK);',
            self.__db_name
        )
        if len(query_result) == 0:
            return 0
        return query_result[0].get('row_count')

    @staticmethod
    def __get_connection_string_params(connection_string) -> dict:
        connection_string_params = {}
        for part in connection_string.split(';'):
            key_value_pair_array = part.split('=')
            if len(key_value_pair_array) != 2:
                continue
            if key_value_pair_array[0] == 'SERVER':
                host_and_port = key_value_pair_array[1].split(',')
                connection_string_params['SERVER'] = host_and_port[0]
                if len(host_and_port) == 2:
                    connection_string_params['PORT'] = int(host_and_port[1])
            else:
                connection_string_params[key_value_pair_array[0]] = key_value_pair_array[1]
        return connection_string_params
