import pytest
from assertpy import assert_that

from mssql import EphemeralMsSqlDbContextBuilder


class TestInitializingContextShould:

    def test_throw_exception_when_data_source_is_not_ocal(self):
        with pytest.raises(Exception) as e:
            with EphemeralMsSqlDbContextBuilder()\
                    .build('DRIVER={ODBC Driver 17 for SQL Server};SERVER=10.142.1.11;UID=sa;PWD=my-New-pwd;'):
                pass
        assert_that(str(e.value)).is_equal_to('Ephemeral database server must be local, use localhost or 127.0.0.1 as server address.')

    def test_throw_exception_when_database_name_is_present(self):
        with pytest.raises(Exception) as e:
            with EphemeralMsSqlDbContextBuilder()\
                    .build('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,31433;UID=sa;PWD=my-New-pwd;DATABASE=mydb'):
                pass
        assert_that(str(e.value)).is_equal_to('Ephemeral database name should not be included on the connection string, please remove DATABASE parameter.')
