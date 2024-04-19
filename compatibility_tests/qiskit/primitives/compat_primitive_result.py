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
from typing import Any, TypeVar
from pytest_asdf_fixtures import save_fixture
import numpy as np
from qiskit.primitives.containers import DataBin, PubResult, PrimitiveResult

from asdf_qiskit.tests.utils import assertDataBinEqual


@pytest.fixture(params=[10])
@save_fixture
def primitive_result(request) -> PrimitiveResult[PubResult]:
    num_results = request.param
    if num_results <= 0:
        raise ValueError("num_results must be a positive non-zero integer.")
    if num_results > 26:
        raise NotImplementedError(
            f"{__name__} cannot generate list of PubResults for more than 26."
        )
    _pub_results = [
        PubResult(
            DataBin(shape=(size, size), **{key: np.ones((size, size)) * i_key}),
            metadata={"key": key},
        )
        for size, (i_key, key) in zip(
            range(4, num_results + 4),
            enumerate("ABCDEFGHJIKLMNOPQRSTUVWXYZ"),
        )
    ]
    metadata = {"num_results": num_results, "some_other_parameter": "3.14159265258976"}
    return PrimitiveResult(pub_results=_pub_results, metadata=metadata)


def compat_tuple_ints(
    primitive_result: PrimitiveResult[PubResult], saved_fixtures: dict[str, Any]
):
    output = saved_fixtures["primitive_result"]
    pubs = primitive_result._pub_results
    metadata = primitive_result.metadata
    assert isinstance(output, PrimitiveResult), (
        "Round trip object is not a PrimitiveResult instance."
    )
    assert len(pubs) == len(output._pub_results), "Number of PubResults is incorrect."

    for i_res, (in_res, out_res) in enumerate(zip(pubs, output._pub_results)):
        assert isinstance(out_res, PubResult), (
            f"pub {i_res} is not a PubResult instance."
        )
        try:
            assertDataBinEqual(in_res.data, out_res.data)
        except Exception as e:
            raise ValueError(f"pub {i_res} data is not the same.", e)
        assert in_res.metadata == out_res.metadata, (
            f"pub {i_res} metadata is not the same."
        )

    assert metadata == output.metadata, "Roundtrip metadata is not the same."
