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
from qiskit.quantum_info import PauliList
import numpy as np


@pytest.fixture(params=[(1, 1), (8, 1), (1, 10), (100, 100), (1, 100), (100, 1)])
@save_fixture
def pauli_list(request) -> PauliList:
    num_terms, num_qubits = request.param
    rng = np.random.default_rng(seed=271828)
    if num_terms <= 0:
        raise ValueError("num_terms must be a positive non-zero integer.")
    if num_qubits > 200:
        raise NotImplementedError(
            f"{__name__} cannot generate PauliList for more than 200 num_qubits in tests."
        )
    _paulis = [
        "".join(x) for x in rng.choice(list("IXYZ"), size=(num_terms, num_qubits))
    ]
    return PauliList(data=_paulis)


def compat_tuple_ints(pauli_list: PauliList, saved_fixtures: dict[str, Any]):
    result = saved_fixtures["pauli_list"]
    assert isinstance(result, PauliList), (
        "Round trip object is not a PauliList instance."
    )
    assert len(pauli_list) == len(result), "Number of Paulis is incorrect."
    assert pauli_list.num_qubits == result.num_qubits, "Number of qubits is incorrect."
    assert pauli_list == result, "PauliLists aren't equivalent."
