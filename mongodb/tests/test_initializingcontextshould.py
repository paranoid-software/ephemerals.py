import pytest
from assertpy import assert_that

from mongodb import ConnectionParams, EphemeralMongoDbContextBuilder


class TestInitializingContextShould:

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

    def test_fail_when_db_name_is_not_allowed(self, connection_params):
        with pytest.raises(Exception, match='Database name admin is not allowed !'):
            with EphemeralMongoDbContextBuilder().build(connection_params, 'admin'):
                pass
