# ******************************************************************************
#  Copyright (c) 2020 University of Stuttgart
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************

from mqt import qecc
from qiskit import QuantumCircuit
from app.model.error_correction_response import (
    ApplyECCResponse,
)
from app.model.error_correction_request import (
    ApplyECCRequest,
)

# Applies the Error Correction codes to all incoming circuits using the TUM Toolkit
def applyECC(request: ApplyECCRequest):
    list_input = True
    if isinstance(request.circuit, str):
        request.circuit = [request.circuit]
        list_input = False

    ecc_circuits = []
    width = []
    depth = []
    for circuit in request.circuit:
        # converting openqasm2 strings to qiskit circuit objects
        circuit_to_save_to_file = QuantumCircuit().from_qasm_str(circuit)
        circuit_to_save_to_file.qasm(formatted=False, filename="temp_circuit.qasm")

        result = qecc.apply_ecc(
            "./temp_circuit.qasm", request.errorCorrectionCode, request.eccFrequency
        )

        corrected_circ = QuantumCircuit().from_qasm_str(result["circ"])
        ecc_circuits.append(corrected_circ)
        depth.append(corrected_circ.depth())
        width.append(corrected_circ.num_qubits)

    return ApplyECCResponse(
        circuit=ecc_circuits,
        circuit_depth=depth,
        circuit_width=width,
        list_input=list_input,
    )
