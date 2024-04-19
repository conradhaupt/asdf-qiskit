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
    from qiskit.primitives.containers import PrimitiveResult


class PrimitiveResultConverter(Converter):
    """Converter for primitive :class:`~qiskit.primitives.PrimitiveResult` instances.

    Serialised with a list of :class:`~qiskit.primitives.PubResult`
    instances and
    :attr:`~qiskit.primitives.PrimitiveResult._metadata`.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/containers/primitive-result-0.0.0"]
    """YAML tags for :class:`~qiskit.primitives.PrimitiveResult`
    instances."""

    types = ["qiskit.primitives.containers.primitive_result.PrimitiveResult"]
    """Types that are serialisable by
    :class:`PrimitiveResultConverter`."""

    def to_yaml_tree(self, obj: PrimitiveResult, tag, ctx):
        return {"pub_results": obj._pub_results, "metadata": obj._metadata}

    def from_yaml_tree(self, node, tag, ctx):
        from qiskit.primitives.containers import PrimitiveResult

        return PrimitiveResult(
            pub_results=node["pub_results"], metadata=node["metadata"]
        )
