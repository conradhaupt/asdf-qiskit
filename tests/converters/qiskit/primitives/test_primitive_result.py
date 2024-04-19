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
from qiskit.primitives.containers import DataBin, PubResult, PrimitiveResult
import numpy as np


class TestPrimitiveResult(TestCase):
    @classmethod
    def generate_pub_results(cls, num_results: int) -> list[PubResult]:
        if num_results <= 0:  # pragma: no cover
            raise ValueError("num_results must be a positive non-zero integer.")
        if num_results > 26:  # pragma: no cover
            raise NotImplementedError(
                f"{__name__} cannot generate list of PubResults for more than 26."
            )
        return [
            PubResult(
                DataBin(shape=(size, size), **{key: np.ones((size, size)) * i_key}),
                metadata={"key": key},
            )
            for size, (i_key, key) in zip(
                range(4, num_results + 4),
                enumerate("ABCDEFGHJIKLMNOPQRSTUVWXYZ"),
            )
        ]

    def test_roundtrip(self):
        NUM_RESULTS = 10
        pubs = self.generate_pub_results(NUM_RESULTS)
        metadata = {
            "num_results": NUM_RESULTS,
            "some_other_parameter": "3.14159265258976",
        }
        result = PrimitiveResult(pub_results=pubs, metadata=metadata)
        output = roundtrip_object(result)
        self.assertIsInstance(
            output,
            PrimitiveResult,
            "Round trip object is not a PrimitiveResult instance.",
        )
        self.assertEqual(
            len(pubs), len(output._pub_results), "Number of PubResults is incorrect."
        )
        for i_res, (in_res, out_res) in enumerate(zip(pubs, output._pub_results)):
            self.assertTrue(
                isinstance(out_res, PubResult),
                f"pub {i_res} is not a PubResult instance.",
            )
            self.assertDataBinEqual(
                in_res.data, out_res.data, f"pub {i_res} data is not the same."
            )
            self.assertEqual(
                in_res.metadata,
                out_res.metadata,
                f"pub {i_res} metadata is not the same.",
            )
        self.assertEqual(
            metadata, output.metadata, "Roundtrip metadata is not the same."
        )
