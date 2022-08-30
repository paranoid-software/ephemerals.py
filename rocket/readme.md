# Ephemeral Rocket DB Context

Python library to allow databases integration tests with little code.

## PyPi Package

The package is available at PyPi at https://pypi.org/project/ephemerals-rocket/

## Quickstart

To use the library we must install it by using PyPi:

```shell
pip install ephemerals-rocket
```

Then we can reference the package on our test classes and start using it.

```python
import pytest
from assertpy import assert_that

from ephemeralsrocket import Credentials, ConnectionParams, EphemeralRocketDbContextBuilder


class TestMyTestClass:

    @pytest.fixture
    def connection_params(self):
        return ConnectionParams('http',
                                'localhost',
                                8000,
                                Credentials('sa',
                                            'my-secret',
                                            'master')
                                )

    def test_my_test_method(self, connection_params):
        with EphemeralRocketDbContextBuilder()\
                .add_items('books', [{'name': 'My first book'}])\
                .build(connection_params) as (ctx, db_name, init_errors):
            # Perform our tests and asserts using the provisioned database
            pass
    
```

In the code shown above:

- EphemeralRocketDbContextBuilder() # Will create a context builder.
- .add_items('books', [{'name': 'My first book'}]) # Will set a book item creation.
- .build(connection_params) as (ctx, db_name, init_errors) # Will execute all registered commands using the provided connection_params and will return the context, database name and initilization errors.

Finaly when the ephemeral DB context is disposed the created database will be DROPPED.
