from unittest import mock
import pytest
from assertpy import assert_that

from mssql import EphemeralMsSqlDbContextBuilder, DbManagerProtocol, FilesManagerProtocol


class TestBuildingContextShould:

    @pytest.fixture
    def connection_string(self):
        return 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost,31433;UID=sa;PWD=my-New-pwd;'

    def test_set_ephemeral_db_name_prefix(self, connection_string):
        with EphemeralMsSqlDbContextBuilder()\
                .build(connection_string) as (ctx, db_name, scripts_errors):
            assert_that(db_name).starts_with('edb')

    def test_execute_one_command_per_added_script(self, connection_string):
        db_manager = mock.Mock(spec=DbManagerProtocol)
        with EphemeralMsSqlDbContextBuilder()\
                .add_script('CREATE TABLE test (id INT);')\
                .add_script('INSERT INTO test VALUES(1);')\
                .build(connection_string, db_manager):
            assert_that(db_manager.execute_non_query.call_count).is_equal_to(2)

    def test_create_test_table(self, connection_string):
        with EphemeralMsSqlDbContextBuilder()\
                .add_script('CREATE TABLE test (id INT);') \
                .add_script('INSERT INTO test VALUES(1);') \
                .build(connection_string) as (ctx, db_name, scripts_errors):
            assert_that(ctx.get_all_table_names()).contains('test')

    def test_create_2_test_table_rows(self, connection_string):
        with EphemeralMsSqlDbContextBuilder()\
                .add_script('CREATE TABLE test (id INT);') \
                .add_script('INSERT INTO test VALUES(1);') \
                .add_script('INSERT INTO test VALUES(2);') \
                .build(connection_string) as (ctx, db_name, scripts_errors):
            assert_that(ctx.get_row_count('test')).is_equal_to(2)

    def test_read_one_script_file(self, connection_string):
        files_manager = mock.Mock(spec=FilesManagerProtocol)
        db_manager = mock.Mock(spec=DbManagerProtocol)
        with EphemeralMsSqlDbContextBuilder(files_manager)\
                .add_script_from_file('my-script.sql')\
                .add_script('INSERT INTO test VALUES(1);')\
                .build(connection_string, db_manager):
            files_manager.read_all_text.assert_called_once()

    def test_create_ephemeral_database(self, connection_string):
        with EphemeralMsSqlDbContextBuilder()\
                .build(connection_string) as (ctx, db_name, scripts_errors):
            assert_that(ctx.get_all_database_names()).contains(db_name)
        assert_that(ctx.get_all_database_names()).does_not_contain(db_name)
