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

import itertools as it

import ddt
import numpy as np
from asdf_qiskit.tests import TestCase
from asdf_qiskit.tests.utils import roundtrip_object
from qiskit.primitives.containers import BitArray


@ddt.ddt
class TestBitArray(TestCase):
    @classmethod
    def generate_bitarray(
        cls, shape: tuple[int, ...], num_shots: int, num_bits: int, seed: int = 3141
    ) -> BitArray:
        rng = np.random.default_rng(seed=seed)
        data = rng.choice(
            [False, True], size=(*shape, num_shots, num_bits), p=[0.5, 0.5]
        )
        return BitArray.from_bool_array(data)

    @ddt.idata(
        [
            (_shape, _num_shots, _num_bits, _lazy_load)
            for _shape, _num_shots, _num_bits, _lazy_load in it.product(
                [(), (1,), (10, 10), (100, 10)],
                [16, 32, 128],
                [1, 4, 16, 100],
                [False, True],
            )
        ]
    )
    @ddt.unpack
    def test_roundtrip(
        self, shape: tuple[int, ...], num_shots: int, num_bits: int, lazy_load: bool
    ):
        arr = self.generate_bitarray(
            shape=shape, num_shots=num_shots, num_bits=num_bits
        )
        result = roundtrip_object(arr, lazy_load=lazy_load)
        self.assertIsInstance(
            result,
            BitArray,
            "Round trip object is not a BitArray instance.",
        )
        self.assertEqual(arr.shape, result.shape, "Shapes differ.")
        self.assertEqual(arr.num_shots, result.num_shots, "num_shots differ.")
        self.assertEqual(arr.num_bits, result.num_bits, "num_bits differ.")
        self.assertEqual(arr, result, "Round trip object is different.")
