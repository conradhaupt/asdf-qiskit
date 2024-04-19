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

from enum import Enum
from typing import TYPE_CHECKING

from asdf.extension import Converter

if TYPE_CHECKING:
    from qiskit.quantum_info.operators.symplectic.sparse_pauli_op import SparsePauliOp


class Sparsity(Enum):
    ALL_NUMPY = 0
    AS_LIST = 1


class SparsePauliOpConverter(Converter):
    """Converter for :class:`~qiskit.quantum_info.SparsePauliOp` instances.

    Though :class:`~qiskit.quantum_info.SparsePauliOp` stores Paulis as a
    :class:`PauliList`, this converter serialises them differently. Both the
    Paulis and the coefficients can be stored inline or as numpy arrays. The
    minimum number of Paulis, i.e., number of qubits multiplied by number of
    terms, to use the symplectic representation is defined by
    :attr:`MIN_PAULIS_NUMPY`. The minimum number of terms to represent the
    coefficients as a numpy array is defined by :attr:`MIN_COEFFS_NUMPY`.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/quantum_info/sparsepauliop-0.0.0"]
    """YAML tags for :class:`BitArray` instances."""

    types = [
        "qiskit.quantum_info.operators.symplectic.sparse_pauli_op.SparsePauliOp",
    ]
    """Types that are serialisable by :class:`BitArrayConverter`."""

    MIN_PAULIS_NUMPY = 8 * 8
    """Minimum number of Paulis to use the numpy representation for Paulis.

    Calculated as the number of qubits multiplied by the number of terms.
    """

    MIN_COEFFS_NUMPY = 16
    """Minimum number of terms to use the numpy representation for coefficients."""

    def __determine_sparsity(
        self, obj: SparsePauliOp, tag, ctx
    ) -> tuple[Sparsity, Sparsity]:
        if len(obj.paulis) * obj.num_qubits > self.MIN_PAULIS_NUMPY:
            __paulis_sparsity = Sparsity.ALL_NUMPY
        else:
            __paulis_sparsity = Sparsity.AS_LIST
        if len(obj.paulis) > self.MIN_COEFFS_NUMPY:
            __coeffs_sparsity = Sparsity.ALL_NUMPY
        else:
            __coeffs_sparsity = Sparsity.AS_LIST
        return __paulis_sparsity, __coeffs_sparsity

    def to_yaml_tree(self, obj: SparsePauliOp, tag, ctx):
        import numpy as np

        __paulis_sparsity, __coeffs_sparsity = self.__determine_sparsity(obj, tag, ctx)

        paulis = obj.paulis
        # Handle coefficients
        coeffs = obj.coeffs
        if np.any(paulis.phase != 1):
            # Push phases into coefficients
            coeffs *= np.array([1, -1j, -1, 1j])[paulis.phase]
        # *** Handle paulis

        tree = {
            "num_qubits": obj.num_qubits,
        }
        if __paulis_sparsity == Sparsity.ALL_NUMPY:
            tree["x"] = paulis.x
            tree["z"] = paulis.z
        else:
            tree["paulis"] = [str(x).replace("-", "").replace("i", "") for x in paulis]
        if __coeffs_sparsity == Sparsity.ALL_NUMPY:
            tree["coeffs"] = coeffs
        else:
            from asdf._core._converters.complex import ComplexConverter

            complex_converter = ComplexConverter()
            tree["coeffs"] = [
                complex_converter.to_yaml_tree(x, tag, ctx) for x in coeffs
            ]
        return tree

    def from_yaml_tree(self, node, tag, ctx):
        import numpy as np
        from asdf.tags.core.ndarray import NDArrayType
        from qiskit.quantum_info.operators.symplectic.sparse_pauli_op import (
            PauliList,
            SparsePauliOp,
        )

        # num_qubits = node["num_qubits"]

        # *** Deserialise Paulis
        if "x" in node and "z" in node:
            _z = node["z"]
            _x = node["x"]
            if _z.shape != _x.shape:
                raise ValueError("Symplectic paulis have mismatching shapes.")

            num_terms = int(_z.shape[0])
            _phase = np.zeros((_z.shape[0],), dtype=int)
            paulis = PauliList.from_symplectic(z=_z, x=_x, phase=_phase)
        elif "paulis" in node:
            paulis = PauliList(node["paulis"])
            num_terms = len(paulis)
        else:
            raise ValueError("Malformed SparsePauliOp")

        # *** Deserialise Coefficients
        if "coeffs" not in node:
            raise ValueError("Malformed SparsePauliOp")
        _coeffs = node["coeffs"]
        # If we have an NDArrayType, which is used for lazy loading, we need to
        # convert it to an explicit Numpy Array. SparsePauliOp does some
        # type-checking on _coeffs.dtype which requires an instance of ndarray
        # and not NDArrayType.
        if isinstance(_coeffs, NDArrayType):
            _coeffs = _coeffs._make_array()

        if isinstance(_coeffs, list):
            if len(_coeffs) != num_terms:
                raise ValueError(
                    "Number of SparsePauliOp coefficients doesn't match the number of Pauli strings."
                )
            from asdf._core._converters.complex import ComplexConverter

            complex_converter = ComplexConverter()
            _coeffs = [complex_converter.from_yaml_tree(x, tag, ctx) for x in _coeffs]
        elif isinstance(_coeffs, np.ndarray) and _coeffs.shape[0] != num_terms:
            raise ValueError(
                "Number of SparsePauliOp coefficients doesn't match the number of Pauli strings."
            )
        return SparsePauliOp(data=paulis, coeffs=_coeffs)
