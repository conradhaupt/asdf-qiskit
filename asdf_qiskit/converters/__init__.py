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

"""
==========================================
Converters (:mod:`asdf_qiskit.converters`)
==========================================

.. currentmodule:: asdf_qiskit.converters

This module contains converter definitions for native Python classes, as well as
Qiskit and Qikit IBM Runtime classes.


Core Converters
***************

These converters provide support for generic types that are not necessarily
quantum related.

.. autosummary::
    :toctree:

    core.TupleConverter
    core.UUIDConverter

Qiskit Converters
*****************

Converters for Qiskit are grouped, roughly, by their submodules.

Core
====

.. autosummary::
    :toctree:

    qiskit.circuit.QuantumCircuitConverter


Primitive Containers
====================

.. autosummary::
    :toctree:

    qiskit.containers.BitArrayConverter
    qiskit.containers.DataBinConverter
    qiskit.containers.PrimitiveResultConverter
    qiskit.containers.PubResultConverter


Quantum Info
============

.. autosummary::
    :toctree:

    qiskit.quantum_info.PauliListConverter
    qiskit.quantum_info.SparsePauliOpConverter


"""
