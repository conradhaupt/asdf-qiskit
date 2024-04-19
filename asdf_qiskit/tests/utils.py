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

from io import BytesIO
from typing import TYPE_CHECKING
from unittest import TestCase as UnitTestTestCase

import asdf

if TYPE_CHECKING:
    from qiskit.primitives.containers import DataBin


def roundtrip_object(obj, version=None, lazy_load: bool = False):
    """Add the specified object to an AsdfFile's tree, write the file to
    a buffer, then read it back in and return the deserialized object.

    Args:
        obj: The object to round-trip.
        version: Optional version of the ASDF file to serialise to. Defaults to
            None.
        lazy_load: Whether the ASDF file should be opened with lazy_load.
            Defaults to False.

    Returns:
        The round-trip object, having been serialised and deserialised.
    """
    buff = BytesIO()
    with asdf.AsdfFile(version=version) as af:
        af["obj"] = obj
        af.write_to(buff)

    buff.seek(0)
    with asdf.open(buff, lazy_load=lazy_load, memmap=False) as af:
        return af["obj"]


def assertDataBinEqual(
    databin1: "DataBin", databin2: "DataBin", msg: str | None = None
):
    """Standard Python nassert version of :meth:`TestCase.assertDataBinEqual`.

    Used in compatibility tests where TestCase is not compatible with pytest.

    Args:
        databin1 (DataBin): The first databin.
        databin2 (DataBin): The second databin.
        msg (str, optional): Optional message to include in error messages. Defaults to None.

    Raises:
        self.failureException: If numpy arrays cannot be compared.
    """
    import numpy as np
    from qiskit.primitives.containers import DataBin

    assert isinstance(databin1, DataBin), "databin1 is not a DataBin."
    assert isinstance(databin2, DataBin), "databin2 is not a DataBin."
    assert databin1.shape == databin2.shape, "DataBin shapes are not the same."
    assert databin1.keys() == databin2.keys(), "DataBins contain different keys."

    for key in databin1.keys():
        val1 = getattr(databin1, key)
        val2 = getattr(databin2, key)
        if isinstance(val1, np.ndarray):
            try:
                assert (
                    val1.shape == val2.shape
                ), f"DataBin values for {key} have different shapes."
                assert np.all(
                    val1 == val2
                ), f"DataBin values for {key} arrays are not equal."
                assert (
                    val1.dtype == val2.dtype
                ), f"DataBin values for {key} have different numpy array dtypes."
            except Exception:
                raise AssertionError(f"Failed to compare {key} values as numpy arrays.")
        else:
            assert val1 == val2, f"DataBin values for {key} do not match."


class TestCase(UnitTestTestCase):
    def assertDataBinEqual(self, databin1: "DataBin", databin2: "DataBin", msg=None):
        """Assert that two :class:`~qiskit.primitives.containers.DataBin`
        instances are the same, including their values.

        Args:
            databin1: The first DataBin instance.
            databin2: The second DataBin instance.
            msg: Optional message. Defaults to None.

        Raises:
            If the DataBin instances differ.
        """
        import numpy as np
        from qiskit.primitives.containers import DataBin

        self.assertIsInstance(
            obj=databin1,
            cls=DataBin,
            msg=self._formatMessage(msg, "databin1 is not a DataBin."),
        )
        self.assertIsInstance(
            obj=databin2,
            cls=DataBin,
            msg=self._formatMessage(msg, "databin2 is not a DataBin."),
        )
        self.assertEqual(
            databin1.shape,
            databin2.shape,
            self._formatMessage(msg, "DataBin shapes are not the same."),
        )
        self.assertEqual(
            databin1.keys(),
            databin2.keys(),
            self._formatMessage(msg, "DataBins contain different keys."),
        )
        for key in databin1.keys():
            val1 = getattr(databin1, key)
            val2 = getattr(databin2, key)
            if isinstance(val1, np.ndarray):
                try:
                    self.assertEqual(
                        val1.shape,
                        val2.shape,
                        msg=self._formatMessage(
                            msg, f"DataBin values for {key} have different shapes."
                        ),
                    )
                    self.assertTrue(np.all(val1 == val2))
                    self.assertEqual(
                        val1.dtype,
                        val2.dtype,
                        msg=self._formatMessage(
                            msg,
                            "DataBin values for {key} have different numpy array dtypes.",
                        ),
                    )
                except Exception:
                    raise self.failureException(
                        self._formatMessage(
                            msg, f"Failed to compare {key} values as numpy arrays."
                        )
                    )
            else:
                self.assertEqual(
                    val1,
                    val2,
                    self._formatMessage(msg, f"DataBin values for {key} do not match."),
                )
