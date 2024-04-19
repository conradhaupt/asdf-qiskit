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
import numpy as np
from asdf_qiskit.tests.utils import assertDataBinEqual
from qiskit.primitives.containers import DataBin, PubResult


@pytest.fixture
@save_fixture
def pub_result() -> PubResult:
    return PubResult(DataBin(shape=(10, 10), c=np.ones((10, 10))))


def compat_pub_result(pub_result: PubResult, saved_fixtures: dict[str, Any]):
    output = saved_fixtures["pub_result"]
    assert isinstance(output, PubResult)
    assertDataBinEqual(output.data, pub_result.data)
    assert output.metadata == pub_result.metadata
