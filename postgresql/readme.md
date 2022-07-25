# Ephemeral PostgreSql DB Context

Python library to allow databases integration tests easy coding.

## PyPi Package

The package is available at PyPi at https://pypi.org/project/ephemerals-postgresql/

## Quickstart

To use the library we must install it by using PyPi:

```shell
pip install ephemerals-postgresql
```

Then we can reference the package on our test classes and start using it.

```python
import pytest


from postgresql import EphemeralPostgreSqlDbContextBuilder


class TestMyTestClass:

    @pytest.fixture
    def connection_string(self):
        return 'Server=localhost;Port=35432;User Id=postgres;Password=postgres;'

    def test_my_test_method(self, connection_string):
        with EphemeralPostgreSqlDbContextBuilder()\
                .add_script('CREATE TABLE my_table (id INT, name VARCHAR(128));') \
                .add_script("INSERT INTO my_table VALUES(1, 'Data 1');") \
                .add_script("INSERT INTO my_table VALUES(2, 'Data 2');") \
                .build(connection_string) as (ctx, db_name):
            ephemeral_db_name = db_name
            # Perform our tests and asserts using the provisioned database
```

In the code shown above:

- EphemeralMsSqlDbContextBuilder() # Will create a context builder.
- add_script('CREATE TABLE my_table (id INT, name VARCHAR(128));') # Will set a table creation script for a table with the name "my_table" which will have two columns (id and name)
- add_script("INSERT INTO my_table VALUES(1, 'Data 1');") # Will set a record addning script into the "my_table" table.
- add_script("INSERT INTO my_table VALUES(2, 'Data 2');") # Will set another record adding script into the "my_table" table.
- build(connection_string) as (ctx, db_name) # Will execute all register scripts using the provided connection_string and will return the context and the newly created database name.

When the ephemeral DB context is disposed the created database will be DROPPED.
