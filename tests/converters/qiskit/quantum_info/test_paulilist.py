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

from asdf_qiskit.tests import TestCase

import ddt
from asdf_qiskit.tests.utils import roundtrip_object
from qiskit.quantum_info import PauliList
import numpy as np


@ddt.ddt
class TestPauliList(TestCase):
    @classmethod
    def generate_paulilist(
        cls, num_terms: int, num_qubits: int, seed: int = 3141
    ) -> PauliList:
        rng = np.random.default_rng(seed=seed)
        if num_terms <= 0:  # pragma: no cover
            raise ValueError("num_terms must be a positive non-zero integer.")
        if num_qubits > 200:  # pragma: no cover
            raise NotImplementedError(
                f"{__name__} cannot generate PauliList for more than 200 num_qubits in tests."
            )
        _paulis = [
            "".join(x) for x in rng.choice(list("IXYZ"), size=(num_terms, num_qubits))
        ]
        return PauliList(data=_paulis)

    @ddt.idata([(1, 1), (8, 1), (1, 10), (100, 100), (1, 100), (100, 1)])
    @ddt.unpack
    def test_roundtrip(self, num_terms: int, num_qubits: int):
        op = self.generate_paulilist(num_terms=num_terms, num_qubits=num_qubits)
        result = roundtrip_object(op)
        self.assertIsInstance(
            result,
            PauliList,
            "Round trip object is not a PauliList instance.",
        )
        self.assertEqual(len(op), len(result), "Number of Paulis is incorrect.")
        self.assertEqual(
            op.num_qubits, result.num_qubits, "Number of qubits is incorrect."
        )
        self.assertEqual(op, result, "PauliLists aren't equivalent.")
