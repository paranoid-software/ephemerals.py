from assertpy import assert_that

from mssql import EphemeralMsSqlDbContextBuilder


class TestBuildingContextShould:

    def test_set_randon_db_name(self):
        with EphemeralMsSqlDbContextBuilder()\
                .build('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,31433;UID=sa;PWD=my-New-pwd;') as db_name:
            assert_that(db_name).starts_with('edb')
