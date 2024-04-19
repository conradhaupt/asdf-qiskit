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

from asdf_qiskit.tests import TestCase
from asdf_qiskit.tests.utils import roundtrip_object
from qiskit.primitives.containers import DataBin, PubResult
import numpy as np


class TestPubResult(TestCase):
    def test_roundtrip(self):
        obj = PubResult(DataBin(shape=(10, 10), c=np.ones((10, 10))))
        output = roundtrip_object(obj)
        self.assertTrue(isinstance(output, PubResult))
        self.assertDataBinEqual(output.data, obj.data)
        self.assertEqual(output.metadata, obj.metadata)
