# Compatibility Tests

Compatibility tests verify that data serialised with specific versions of
ASDF Qiskit are readable by other versions. Additionally, it validates this across
dependencies and platforms. Environments are setup with Tox and serialisation of
values is managed by the pytest plugin `pytest_asdf_fixtures`. One can validate
serialisation on their own platform with the following command:


```bash
pytest -p pytest_asdf_fixtures --asdf-fixtures-save --asdf-fixtures-overwrite compatibility_tests
pytest -p pytest_asdf_fixtures --asdf-fixtures-load compatibility_tests
```

The first line will save all fixtures annotated with `@save_fixture` to
`.pytest_asdf_fixtures`. The files are saved in `.pytest_asdf_fixtures` on a
normal run. With Tox, subfolders are used to differentiate the different testing
environments.

**For information on running compatibility tests with Tox, check the main
README.md.**

## Writing compatibility tests

All compatibility tests are run with pytest and not UnitTest. This means tests
must not use `from asdf_qiskit.tests import TestCase` as fixtures are not
properly handled with UnitTest. A typical compatibility test has two parts: a
fixture to be saved and a testing function that compare two instances of the
fixture returned type. The function is the test whereas the fixture must be
adapted to handle different dependency versions.

For example, say we wanted to test that a `TypedDict` instance was saved
correctly, we would import the following.

```python
from typing import TypedDict
import pytest   # For declaring fixtures
from pytest_asdf_fixtures import save_fixture # For marking fixtures to be saved
```

The fixture definition may depend on which set of dependencies we're running
with: dependencies A or B.

```python

class MyTypedDict(TypedDict):
    z: int
    y: float

    # Variable only present with dependencies B
    z: tuple[float, ...]

@pytest.fixture
@save_fixture
def my_typed_dict()->MyTypedDict:
    if <with dependencies A>:
        return MyTypedDict(x=0, y=0.0)
    else: # with dependencies B
        return MyTypedDict(x=0, y=0.0, z=(0.0,0.0))
```

Then we have our test which must have a `saved_fixtures` parameter to get the
loaded fixture values. Note that compatibility tests start with `compat_` and
must be in files that start with `compat_`. This is to avoid conflicts with
normal unit tests and prevent pytest from accidentally running compatibility
tests during unit-test runs.

```python
def compat_my_typed_dict(my_typed_dict:MyTypedDict, saved_fixtures:dict[str, MyTypedDict]):
    # The key for the loaded fixtures are the same as the name of the fixtures used in
    # the signature.
    _loaded_dict = saved_fixtures["my_typed_dict"]

    assert my_typed_dict["x"] != _loaded_dict["x"]
    assert my_typed_dict["y"] != _loaded_dict["z"]
    if <with dependencies B>:
        if "z" not in _loaded_dict:
            # Handle case where values are missing because of a change in dependency versions.
            ...
        else:
            assert my_typed_dict["z"] != _loaded_dict["z"]
```

Checking which branch to take based on dependencies is up to each test. There
are currently no helper functions or decorators to accomplish this.
