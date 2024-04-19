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
    from qiskit.primitives.containers import PubResult


class PubResultConverter(Converter):
    """Converter for primitive :class:`~qiskit.primitives.PubResult` instances.

    Serialised with :attr:`~qiskit.primitives.PubResult._data` and
    :attr:`~qiskit.primitives.PubResult._metadata`.
    """

    tags = ["asdf://qiskit.org/asdf/tags/qiskit/containers/pub-result-0.0.0"]
    """YAML tags for :class:`~qiskit.primitives.PubResult` instances."""

    types = ["qiskit.primitives.containers.pub_result.PubResult"]
    """Types that are serialisable by
    :class:`~qiskit.primitives.PubResultConverter`."""

    def to_yaml_tree(self, obj: PubResult, tag, ctx):
        return {"data": obj._data, "metadata": obj._metadata}

    def from_yaml_tree(self, node, tag, ctx):
        from qiskit.primitives.containers import PubResult

        return PubResult(data=node["data"], metadata=node["metadata"])
