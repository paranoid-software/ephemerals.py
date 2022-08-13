import pytest
from assertpy import assert_that

from rocket import EphemeralRocketDbContextBuilder


class TestBuildingContextShould:

    @pytest.fixture
    def db_context(self):
        return {
            'baseEndpoint': 'http://192.168.1.77:9000',
            'account': {
                'secret': 'qhp3mDb85Hfo0kJ7W1x136TCjrfNTQ0la_Du9FIkKzMEdizE0f4A-htl9MLS4jBFbmtCPo_oA1sZOajTd0O-rQ',
                'grantType': 'master'
            }
        }

    def test_set_ephemeral_db_name_prefix(self, db_context):
        with EphemeralRocketDbContextBuilder()\
                .add_encrypt_definitions('tests', {'properties': ['createdAt', 'lastModifiedAt']}) \
                .add_date_properties_definitions('tests', {'properties': ['createdAt', 'lastModifiedAt']}) \
                .add_search_definitions('tests', {'properties': {}, 'exclude': ['createdAt', 'lastModifiedAt']})\
                .build(db_context) as (ctx, app_name, master_access_token):
            assert_that(app_name).starts_with('edb')
