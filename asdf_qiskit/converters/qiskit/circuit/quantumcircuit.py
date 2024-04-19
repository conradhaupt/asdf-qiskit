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

from __future__ import annotations

from typing import TYPE_CHECKING

from asdf.extension import Converter

if TYPE_CHECKING:
    from qiskit.circuit import QuantumCircuit


class QuantumCircuitConverter(Converter):
    """Converter for single :class:`~qiskit.circuit.QuantumCircuit` instances.

    Note that lists of quantum circuits are not serialised together.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/circuit/quantumcircuit-0.0.0"]
    """YAML tags for quantum circuits."""

    types = ["qiskit.circuit.QuantumCircuit"]
    """Types that are serialisable by :class:`QuantumCircuitConverter`."""

    def to_yaml_tree(self, obj: QuantumCircuit, tag, ctx):
        from io import BytesIO
        import numpy as np
        from qiskit.qpy import dump

        __qpy = BytesIO()
        dump(obj, __qpy)
        __qpy.seek(0)
        qpy_bytes = np.frombuffer(__qpy.read(), dtype=np.uint8)
        return {
            "name": obj.name,
            "num_qubits": obj.num_qubits,
            "num_clbits": obj.num_clbits,
            "qpy": qpy_bytes,
        }

    def from_yaml_tree(self, node, tag, ctx):
        from qiskit.qpy import load
        import numpy as np
        from io import BytesIO

        # name, num_qubits, and num_clbits aren't used to decode qpy; so we ignore them.
        qpy_bytes = np.array(node["qpy"])
        __qpy = BytesIO(qpy_bytes.tobytes())
        __circuit = load(__qpy)
        return __circuit[
            0
        ]  # Always returns a list, but we only serialise single circuits.
