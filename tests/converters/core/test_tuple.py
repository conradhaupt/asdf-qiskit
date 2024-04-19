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


class TestTupleConverter(TestCase):
    def test_roundtrip_ints(self):
        _tuple = (0, 1, 2, 3, 4)
        _rt_tuple = roundtrip_object(_tuple)
        self.assertEqual(_tuple, _rt_tuple)

    def test_roundtrip_floats(self):
        _tuple = (0.0, 1.0, 2.0, 3.0, 4.0)
        _rt_tuple = roundtrip_object(_tuple)
        self.assertEqual(_tuple, _rt_tuple)

    def test_roundtrip_strings(self):
        _tuple = ("0", "1", "2", "3", "4")
        _rt_tuple = roundtrip_object(_tuple)
        self.assertEqual(_tuple, _rt_tuple)

    def test_roundtrip_nested(self):
        _tuple = ((0, 1, 0), 9, (0.4, "87"))
        _rt_tuple = roundtrip_object(_tuple)
        self.assertEqual(_tuple, _rt_tuple)
