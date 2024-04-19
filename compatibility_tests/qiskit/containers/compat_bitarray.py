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

import pytest
from typing import Any
from pytest_asdf_fixtures import save_fixture
from qiskit.primitives.containers import BitArray
import numpy as np
import itertools as it


@pytest.fixture(
    params=[
        (_shape, _num_shots, _num_bits)
        for _shape, _num_shots, _num_bits in it.product(
            [(), (1,), (10, 10), (100, 10)], [16, 32, 128], [1, 4, 16, 100]
        )
    ]
)
@save_fixture
def bitarray_tuple(request) -> tuple[BitArray, tuple[int, ...], int, int]:
    shape, num_shots, num_bits = request.param
    rng = np.random.default_rng(seed=271828)
    data = rng.choice([False, True], size=(*shape, num_shots, num_bits), p=[0.5, 0.5])
    return BitArray.from_bool_array(data), shape, num_shots, num_bits


def compat_bitarray(
    bitarray_tuple: tuple[BitArray, tuple[int, ...], int, int],
    saved_fixtures: dict[str, Any],
):
    arr, _, _, _ = bitarray_tuple
    loaded_arr, _, _, _ = saved_fixtures["bitarray_tuple"]
    assert isinstance(arr, BitArray), "Loaded object is not a BitArray instance."
    assert loaded_arr.shape == arr.shape, "Shapes differ."
    assert loaded_arr.num_shots == arr.num_shots, "num_shots differ."
    assert loaded_arr.num_bits == arr.num_bits, "num_bits differ."
    assert loaded_arr == arr, "Loaded object is different."
