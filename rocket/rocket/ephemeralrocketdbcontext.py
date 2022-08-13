import uuid

from rocket import DbManagerProtocol, DbManager


class EphemeralRocketDbContext:

    __db_manager: DbManagerProtocol
    __date_time_properties_definitions: dict
    __encrypt_definitions: dict
    __search_definitions: dict
    __items: dict
    __db_name: str = None

    def __init__(self,
                 db_context: dict,
                 date_properties_definitions: dict,
                 encrypt_definitions: dict,
                 search_definitions: dict,
                 items: dict,
                 db_manager: DbManagerProtocol = None):
        self.__db_manager = db_manager or DbManager(db_context)
        self.__date_time_properties_definitions = date_properties_definitions
        self.__encrypt_definitions = encrypt_definitions
        self.__search_definitions = search_definitions
        self.__items = items

    def __enter__(self):
        self.__db_name = f'edb_{uuid.uuid4().hex}'
        self.__db_manager.create_database(self.__db_name)
        initialization_errors = []

        for object_name in self.__date_time_properties_definitions.keys():
            try:
                self.__db_manager.create_date_time_properties_definition(self.__db_name, object_name, self.__date_time_properties_definitions[object_name])
            except Exception as e:
                initialization_errors.append(e)

        for object_name in self.__encrypt_definitions.keys():
            try:
                self.__db_manager.create_encrypt_definition(self.__db_name, object_name, self.__encrypt_definitions[object_name])
            except Exception as e:
                initialization_errors.append(e)

        for object_name in self.__search_definitions.keys():
            try:
                m = self.__db_manager.create_search_definition(self.__db_name, object_name, self.__search_definitions[object_name])
            except Exception as e:
                initialization_errors.append(e)

        for object_name in self.__items.keys():
            for payload in self.__items[object_name]:
                try:
                    self.__db_manager.exec_post(self.__db_name, object_name, payload)
                except Exception as e:
                    initialization_errors.append(e)
        return None, self.__db_name, None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__db_manager.drop_database(self.__db_name)
