# This code is part of ASDF Qiskit.
#
# Copyright 2024-2025 Conrad Haupt <conrad@conradhaupt.com> and IBM.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from typing import Any
from pytest_asdf_fixtures import save_fixture


@pytest.fixture(params=[int, float, str, tuple])
@save_fixture
def _tuple(request) -> tuple[Any, ...]:
    _type = request.param
    if _type == int:
        return (0, 1, 2, 3, 4)
    elif _type == float:
        return (0.0, 1.0, 2.0, 3.0, 4.0)
    elif _type == str:
        return ("0", "1", "2", "3", "4")
    elif _type == tuple:
        return ((0, 1, 0), 9, (0.4, "87"))
    raise NotImplementedError("Tuple of '{}' types not supported.".format(str(_type)))


def compat_tuple_different_types(
    _tuple: tuple[int | float | str | tuple[Any], ...], saved_fixtures: dict[str, Any]
):
    _msg = "Loaded tuple filled with {} instances is incorrect.".format(str(_tuple))
    assert _tuple == saved_fixtures["_tuple"], _msg
