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
from asdf.extension import Converter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from qiskit.primitives.containers import DataBin


class DataBinConverter(Converter):
    """Converter for :class:`~qiskit.primitives.DataBin` instances.

    Instances are serialised as a mapping containing all data entries and a
    tuple of the shape.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/containers/databin-0.0.0"]
    """YAML tags for :class:`~qiskit.primitives.DataBin`
    instances."""

    types = ["qiskit.primitives.containers.data_bin.DataBin"]
    """Types that are serialisable by :class:`DataBinConverter`."""

    def to_yaml_tree(self, obj: DataBin, tag, ctx):
        return {
            "shape": obj._shape,
            **{k: v for k, v in obj.__dict__.items() if k not in ["_shape", "_data"]},
        }

    def from_yaml_tree(self, node, tag, ctx):
        from asdf.tags.core.ndarray import NDArrayType
        from qiskit.primitives import DataBin

        def __converter(value):
            if isinstance(value, NDArrayType):
                return value._make_array()
            return value

        _shape = tuple(node["shape"])
        __data = {k: __converter(v) for k, v in node.items() if k not in ["shape"]}
        return DataBin(
            shape=_shape,
            **__data,
        )
