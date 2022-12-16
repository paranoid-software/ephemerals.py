from unittest import mock

import pytest
from assertpy import assert_that

from mongodb import EphemeralMongoDbContextBuilder, ConnectionParams, FilesManagerProtocol


class TestBuildingContextShould:

    @pytest.fixture
    def connection_params(self):
        return ConnectionParams('localhost', 27017, 'root', 'pwd')

    def test_set_default_ephemeral_db_name_prefix(self, connection_params):
        with EphemeralMongoDbContextBuilder().build(connection_params) as (ctx, db_name, init_errors):
            assert_that(db_name).starts_with('edb_')

    def test_set_know_db_name(self, connection_params):
        with EphemeralMongoDbContextBuilder().build(connection_params, 'my_db_name') as (ctx, db_name, init_errors):
            assert_that(db_name).is_equal_to('my_db_name')

    def test_fail_when_required_db_name_is_not_available(self, connection_params):
        with EphemeralMongoDbContextBuilder().build(connection_params, 'my_db_name'):
            with pytest.raises(Exception, match='Database name my_db_name is already taken !'):
                with EphemeralMongoDbContextBuilder().build(connection_params, 'my_db_name'):
                    pass

    def test_read_one_data_file(self, connection_params):
        files_manager = mock.Mock(spec=FilesManagerProtocol)
        files_manager.read_all_text.return_value = '{"books": [{"name": "Pinocchio"}]}'
        with EphemeralMongoDbContextBuilder(files_manager)\
                .add_items_from_file('books.json')\
                .build(connection_params, 'my_library_db'):
            files_manager.read_all_text.assert_called_once()

    def test_return_1_init_error(self, connection_params):
        files_manager = mock.Mock(spec=FilesManagerProtocol)
        files_manager.read_all_text.return_value = '{"books": [1]}'
        with EphemeralMongoDbContextBuilder(files_manager)\
                .add_items_from_file('books.json')\
                .build(connection_params, 'my_library_db') as (ctx, db_name, init_errors):
            assert_that(init_errors).is_length(1)

    @pytest.mark.parametrize('file_content', ['This is not a json', '{"books": 1}', '{"books": {}}'])
    def test_fail_when_file_has_invalid_content(self, file_content, connection_params):
        files_manager = mock.Mock(spec=FilesManagerProtocol)
        files_manager.read_all_text.return_value = file_content
        with pytest.raises(Exception, match=f'books.json content is not valid !'):
            with EphemeralMongoDbContextBuilder(files_manager)\
                    .add_items_from_file('books.json')\
                    .build(connection_params, 'my_library_db'):
                pass

    def test_create_2_items_at_boooks_collection(self, connection_params):
        with EphemeralMongoDbContextBuilder()\
                .add_items('books', [{
                    'name': 'My first book'
                }, {
                    'name': 'My second book'
                }])\
                .build(connection_params, 'my_library_db') as (ctx, db_name, init_errors):
            assert_that(ctx.count_documents('books')).is_equal_to(2)
