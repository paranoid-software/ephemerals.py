import pytest
from assertpy import assert_that

from postgresql import EphemeralPostgreSqlDbContextBuilder


class TestInitializingContextShould:

    def test_throw_exception_when_data_source_is_not_ocal(self):
        with pytest.raises(Exception) as e:
            with EphemeralPostgreSqlDbContextBuilder()\
                    .build('Server=192.168.1.1;Port=35432;'):
                pass
        assert_that(str(e.value)).is_equal_to('Ephemeral database server must be local, use localhost or 127.0.0.1 as server address.')

    def test_throw_exception_when_database_name_is_present(self):
        with pytest.raises(Exception) as e:
            with EphemeralPostgreSqlDbContextBuilder()\
                    .build('Server=localhost;Port=35432;Database=my_database;'):
                pass
        assert_that(str(e.value)).is_equal_to('Ephemeral database name should not be included on the connection string, please remove DATABASE parameter.')
