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

from enum import Enum
from typing import TYPE_CHECKING

from asdf.extension import Converter

if TYPE_CHECKING:
    from qiskit.quantum_info.operators.symplectic.pauli_list import PauliList


class Sparsity(Enum):
    ALL_NUMPY = 0
    AS_LIST = 1


class PauliListConverter(Converter):
    """Converter for :class:`~qiskit.quantum_info.PauliList` instances.

    Pauli lists are serialised as metadata, identifying the number of qubits,
    and the Paulis themselves. The Paulis are either serialised inline, as
    strings, or as symplectic arrays with ``x``, ``z``, and ``phase`` arrays.
    The minimum number of qubits for the symplectic representation is defined by
    :attr:`MIN_PAULIS_NUMPY`.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/quantum_info/paulilist-0.0.0"]
    """YAML tags for :class:`~qiskit.quantum_info.PauliList` instances."""
    types = ["qiskit.quantum_info.operators.symplectic.pauli_list.PauliList"]
    """Types that are serialisable by :class:`PauliListConverter`."""

    MIN_PAULIS_NUMPY = 8 * 8

    def __determine_sparsity(self, obj: "PauliList", tag, ctx) -> Sparsity:
        if len(obj) * obj.num_qubits > self.MIN_PAULIS_NUMPY:
            __paulis_sparsity = Sparsity.ALL_NUMPY
        else:
            __paulis_sparsity = Sparsity.AS_LIST
        return __paulis_sparsity

    def to_yaml_tree(self, obj: "PauliList", tag, ctx):
        import numpy as np

        __paulis_sparsity = self.__determine_sparsity(obj, tag, ctx)

        tree = {
            "num_qubits": obj.num_qubits,
        }
        if __paulis_sparsity == Sparsity.ALL_NUMPY:
            tree["x"] = obj.x
            tree["z"] = obj.z
            tree["phase"] = obj.phase
        else:
            tree["paulis"] = [str(x) for x in obj]
        return tree

    def from_yaml_tree(self, node, tag, ctx):
        from qiskit.quantum_info.operators.symplectic.pauli_list import (
            PauliList,
        )

        # num_qubits = node["num_qubits"]

        # *** Deserialise Paulis
        if "x" in node and "z" in node and "phase" in node:
            _z = node["z"]
            _x = node["x"]
            _phase = node["phase"]
            if _z.shape != _x.shape:
                raise ValueError("Symplectic paulis have mismatching shapes.")

            # num_terms = int(_z.shape[0])
            paulis = PauliList.from_symplectic(z=_z, x=_x, phase=_phase)
        elif "paulis" in node:
            paulis = PauliList(node["paulis"])
        else:
            raise ValueError("Malformed PauliList")

        return PauliList(data=paulis)
