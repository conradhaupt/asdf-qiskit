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

from asdf.extension import Converter


class TupleConverter(Converter):
    """Simple :class:`tuple` converter.

    YAML doesn't support tuples, which can be treated as arrays in the same way
    as lists. This converter just ensures that the deserialised data is a
    :class:`tuple` and not a :class:`list`.
    """

    tags = ["asdf://qiskit.org/asdf/tags/core/tuple-0.0.0"]
    """YAML tags for tuples."""

    types = [tuple]
    """Types that are serialisable by :class:`TupleConverter`."""

    def to_yaml_tree(self, obj: tuple, tag, ctx):
        return list(obj)

    def from_yaml_tree(self, node, tag, ctx):
        return tuple(node)
