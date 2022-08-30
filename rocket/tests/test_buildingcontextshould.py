import pytest
from assertpy import assert_that

from ephemeralsrocket import Credentials, ConnectionParams, EphemeralRocketDbContextBuilder


class TestBuildingContextShould:

    @pytest.fixture
    def connection_params(self):
        return ConnectionParams('http',
                                '192.168.1.77',
                                9000,
                                Credentials('sa',
                                            'qhp3mDb85Hfo0kJ7W1x136TCjrfNTQ0la_Du9FIkKzMEdizE0f4A-htl9MLS4jBFbmtCPo_oA1sZOajTd0O-rQ',
                                            'master')
                                )

    def test_set_default_ephemeral_db_name_prefix(self, connection_params):
        with EphemeralRocketDbContextBuilder()\
                .build(connection_params) as (ctx, db_name, init_errors):
            assert_that(db_name).starts_with('edb_')

    def test_set_known_db_name(self, connection_params):
        with EphemeralRocketDbContextBuilder()\
                .build(connection_params, 'my_db') as (ctx, db_name, init_errors):
            assert_that(db_name).starts_with('my_db')

    def test_fail_when_db_name_is_already_taken(self, connection_params):
        with pytest.raises(Exception) as e:
            with EphemeralRocketDbContextBuilder()\
                    .build(connection_params, 'my_db'):
                with EphemeralRocketDbContextBuilder() \
                        .build(connection_params, 'my_db'):
                    pass
        assert_that(str(e.value)).is_equal_to('Database name my_db is already taken !')

    def test_fail_when_db_name_is_not_allowed(self, connection_params):
        with pytest.raises(Exception) as e:
            with EphemeralRocketDbContextBuilder()\
                    .build(connection_params, 'admin'):
                pass
        assert_that(str(e.value)).is_equal_to('Database name admin is not allowed !')

    def test_create_2_items_at_boooks_collection(self, connection_params):
        with EphemeralRocketDbContextBuilder()\
                .add_items('books', [{
                    'name': 'My first book'
                }, {
                    'name': 'My second book'
                }])\
                .build(connection_params, 'my_library_db') as (ctx, db_name, init_errors):
            assert_that(ctx.count_records('books')).is_equal_to(2)
