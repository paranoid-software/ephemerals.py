import pytest
from assertpy import assert_that

from mongodb import EphemeralMongoDbContextBuilder, ConnectionParams


class TestBuildingContextShould:

    @pytest.fixture
    def remote_connection_params(self):
        return ConnectionParams('192.12.24.1', 27017, 'root', 'pwd')

    @pytest.fixture
    def connection_params(self):
        return ConnectionParams('localhost', 27017, 'root', 'pwd')

    def test_fail_when_host_name_is_not_allowed(self, remote_connection_params):
        with pytest.raises(Exception, match='Ephemeral database server must be local, use localhost or 127.0.0.1 as host name.'):
            with EphemeralMongoDbContextBuilder().build(remote_connection_params, 'admin'):
                pass

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

    def test_fail_when_db_name_is_not_allowed(self, connection_params):
        with pytest.raises(Exception, match='Database name admin is not allowed !'):
            with EphemeralMongoDbContextBuilder().build(connection_params, 'admin'):
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
