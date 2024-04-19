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
from math import ceil
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qiskit.primitives.containers import BitArray
from asdf.extension import Converter


class BitArrayConverter(Converter):
    """Converter for :class:`~qiskit.primitives.BitArray` instances.

    Instances of :class:`~qiskit.primitives.BitArray` are serialised
    into metadata and a numpy
    array.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/containers/bitarray-0.0.0"]
    """YAML tags for :class:`~qiskit.primitives.BitArray`
    instances."""
    types = ["qiskit.primitives.containers.bit_array.BitArray"]
    """Types that are serialisable by :class:`BitArrayConverter`."""

    def to_yaml_tree(self, obj: BitArray, tag, ctx):
        from asdf._core._converters.ndarray import NDArrayConverter

        _tree = {
            "num_bits": obj._num_bits,
            "num_shots": obj.num_shots,
            "shape": obj.shape,
        }
        _array_tree = NDArrayConverter().to_yaml_tree(
            obj._array.copy(), "tag:stsci.edu:asdf/core/ndarray-1.1.0", ctx=ctx
        )
        if "shape" in _array_tree:
            _expected_shape = (
                *_tree["shape"],
                _tree["num_shots"],
                ceil(_tree["num_bits"] / 8),
            )
            if tuple(_array_tree["shape"]) != _expected_shape:
                raise RuntimeError(
                    "Unexpected shape of internal packed array. Expected {} but got {} instead.".format(
                        _expected_shape, _array_tree["shape"]
                    )
                )
            del _array_tree["shape"]
        _tree["array"] = _array_tree
        return _tree

    def from_yaml_tree(self, node, tag, ctx):
        from qiskit.primitives.containers import BitArray
        from asdf.tags.core.ndarray import NDArrayType
        from asdf._core._converters.ndarray import NDArrayConverter

        _num_bits = node["num_bits"]
        _num_shots = node["num_shots"]
        _shape = node["shape"]
        _array_tree = node["array"]
        _array_shape = (*_shape, _num_shots, ceil(_num_bits / 8))
        _array_tree["shape"] = _array_shape
        _array = NDArrayConverter().from_yaml_tree(
            _array_tree, "tag:stsci.edu:asdf/core/ndarray-1.1.0", ctx=ctx
        )
        if isinstance(_array, NDArrayType):
            _array = _array._make_array()
        return BitArray(array=_array, num_bits=_num_bits)
