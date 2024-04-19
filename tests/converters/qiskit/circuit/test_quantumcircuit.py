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
from asdf_qiskit.tests import TestCase
from asdf_qiskit.tests.utils import roundtrip_object
from qiskit import QuantumCircuit
from qiskit.circuit.random.utils import random_circuit


@ddt.ddt
class TestQuantumCircuitConverter(TestCase):
    @classmethod
    def random_circuit(cls, num_qubits: int, seed: int = 31159) -> QuantumCircuit:
        return random_circuit(
            num_qubits=num_qubits,
            depth=num_qubits,
            measure=True,
            conditional=True,
            reset=True,
            seed=seed,
        )

    @ddt.idata(range(1, 10))
    def test_roundtrip(self, num_qubits: int):
        circuit = self.random_circuit(num_qubits=num_qubits)
        result = roundtrip_object(circuit)
        self.assertIsInstance(
            result,
            QuantumCircuit,
            "Round trip object is not a QuantumCircuit instance.",
        )
        self.assertEqual(circuit, result, "Round trip quantum circuit is different.")
