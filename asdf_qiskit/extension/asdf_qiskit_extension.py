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

from asdf.extension import ManifestExtension

from asdf_qiskit.converters.core.tuple import TupleConverter
from asdf_qiskit.converters.core.uuid import UUIDConverter
from asdf_qiskit.converters.qiskit.circuit import QuantumCircuitConverter
from asdf_qiskit.converters.qiskit.containers.bit_array import BitArrayConverter
from asdf_qiskit.converters.qiskit.containers.data_bin import DataBinConverter
from asdf_qiskit.converters.qiskit.containers.primitive_result import (
    PrimitiveResultConverter,
)
from asdf_qiskit.converters.qiskit.containers.pub_result import PubResultConverter
from asdf_qiskit.converters.qiskit.quantum_info.pauli_list import PauliListConverter
from asdf_qiskit.converters.qiskit.quantum_info.sparsepauliop import (
    SparsePauliOpConverter,
)


class ASDFQiskitExtension(ManifestExtension):
    @property
    def yaml_tag_handles(self):
        return {"!qiskit!": "asdf://qiskit.org/asdf/tags/"}


def get_extensions() -> list["asdf.extension._extension.Extension"]:
    return [
        ASDFQiskitExtension.from_uri(
            "asdf://qiskit.org/asdf/manifests/asdf-qiskit-0.0.0",
            converters=[
                UUIDConverter(),
                QuantumCircuitConverter(),
                DataBinConverter(),
                BitArrayConverter(),
                TupleConverter(),
                PubResultConverter(),
                PrimitiveResultConverter(),
                SparsePauliOpConverter(),
                PauliListConverter(),
            ],
        )
    ]
