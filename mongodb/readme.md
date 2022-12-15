# Ephemeral MongoDB Context

Python library to allow databases integration tests with as little code as possible.

## PyPi Package

The package is available at PyPi at https://pypi.org/project/ephemerals-mongodb/

## Quickstart

To use the library we must install it by using PyPi:

```shell
pip install ephemerals-mongodb
```

Then we can reference the package on our test classes and start using it.

```python
class TestMyTestClass:

    @pytest.fixture
    def connection_params(self):
        return ConnectionParams('localhost', 27017, 'root', 'pwd')

    def test_my_test_method(self, connection_params):
        with EphemeralMongoDbContextBuilder()\
                .add_items('books', [{
                    'name': 'My first book'
                }])\
                .build(connection_params) as (ctx, db_name, init_errors):
            # Perform our tests and asserts using the provisioned database
            pass
```

In the code shown above:

- EphemeralMongoDbContextBuilder() # Will create a context builder.
- .add_items('books', [{'name': 'My first book'}]) # Will set up an operation to create an item or document on the "books" collection.
- .build(connection_params) as (ctx, db_name, init_errors) # Will execute all registered operations using the provided connection_params and will return the context, database name and initilization errors if any.

Finaly when the ephemeral DB context is disposed the created database will be DROPPED.
