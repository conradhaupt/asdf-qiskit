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

import ddt
import numpy as np
from asdf_qiskit.tests import TestCase
from asdf_qiskit.tests.utils import roundtrip_object
from qiskit.quantum_info import SparsePauliOp


@ddt.ddt
class TestSparsePauliOp(TestCase):
    @classmethod
    def generate_sparsepauliop(
        cls, num_terms: int, num_qubits: int, seed: int = 3141
    ) -> SparsePauliOp:
        rng = np.random.default_rng(seed=seed)
        if num_terms <= 0:  # pragma: no cover
            raise ValueError("num_terms must be a positive non-zero integer.")
        if num_qubits > 200:  # pragma: no cover
            raise NotImplementedError(
                f"{__name__} cannot generate SparsePauliOp for more than 200 num_qubits in tests."
            )
        _paulis = [
            "".join(x) for x in rng.choice(list("IXYZ"), size=(num_terms, num_qubits))
        ]
        _coeffs = rng.random(size=(num_terms,)) + 1j * rng.random(size=(num_terms,))
        print(len(_paulis), _coeffs.shape)
        return SparsePauliOp(
            data=_paulis,
            coeffs=_coeffs,
        )

    @ddt.idata([(1, 1), (8, 1), (1, 10), (100, 100), (1, 100), (100, 1)])
    @ddt.unpack
    def test_roundtrip(self, num_terms: int, num_qubits: int):
        op = self.generate_sparsepauliop(num_terms=num_terms, num_qubits=num_qubits)
        result = roundtrip_object(op)
        self.assertIsInstance(
            result,
            SparsePauliOp,
            "Round trip object is not a SparsePauliOp instance.",
        )
        self.assertEqual(
            len(op.paulis), len(result.paulis), "Number of Paulis is incorrect."
        )
        self.assertEqual(
            op.num_qubits, result.num_qubits, "Number of qubits is incorrect."
        )
        self.assertEqual(op, result, "SparsePauliOps aren't equivalent.")

    @ddt.idata([(100, 100), (1, 100), (100, 1)])
    @ddt.unpack
    def test_roundtrip_with_lazy_load(self, num_terms: int, num_qubits: int):
        """Sparsepauliop uses ndarrays in some cases, which supports lazy-loading.

        We only run for large SparsePauliOp instances, where numpy arrays are used.
        """
        op = self.generate_sparsepauliop(num_terms=num_terms, num_qubits=num_qubits)
        result = roundtrip_object(op, lazy_load=True)
        self.assertIsInstance(
            result,
            SparsePauliOp,
            "Round trip object is not a SparsePauliOp instance.",
        )
        self.assertEqual(
            len(op.paulis), len(result.paulis), "Number of Paulis is incorrect."
        )
        self.assertEqual(
            op.num_qubits, result.num_qubits, "Number of qubits is incorrect."
        )
        self.assertEqual(op, result, "SparsePauliOps aren't equivalent.")
