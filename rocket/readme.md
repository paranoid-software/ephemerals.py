# Ephemeral PostgreSql DB Context

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


from rocket import EphemeralRocketDbContextBuilder


class TestMyTestClass:
    pass
```

In the code shown above:

- EphemeralRocketDbContextBuilder() # Will create a context builder.

When the ephemeral DB context is disposed the created database will be DROPPED.
