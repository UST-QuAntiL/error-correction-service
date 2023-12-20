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

from qiskit import qasm3
from mqt import qecc
from qiskit import QuantumCircuit
from qiskit import transpile
from app.model.error_correction_response import (
    ApplyECCResponse,
)
from app.model.error_correction_request import (
    ApplyECCRequest,
)

# Applies the Error Correction codes to all incoming circuits using the TUM Toolkit
def apply_ecc(request: ApplyECCRequest):
    # move individual circuit into list for uniform handling
    list_input = True
    if isinstance(request.circuit, str):
        request.circuit = [request.circuit]
        list_input = False

    # convert string to circuit
    if request.circuitFormat == "openqasm2":
        circuits = [
            QuantumCircuit().from_qasm_str(circuit) for circuit in request.circuit
        ]
    elif request.circuitFormat == "openqasm3":
        circuits = [qasm3.dumps(circuit) for circuit in request.circuit]
    else:
        return "Currently only openqasm2 and openqasm3 are supported as circuit formats"

    # transpile circuits for gates supported by the selected method
    transpiled_circuits = transpile_for_supported_gates(
        circuits, request.errorCorrectionCode
    )

    ecc_circuits = []
    width = []
    depth = []
    for circuit in transpiled_circuits:
        circuit.qasm(formatted=False, filename="temp_circuit.qasm")

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


def transpile_for_supported_gates(circuits, error_correction_code):
    identity_gate = ["id"]
    pauli_gates = ["x", "y", "z"]
    controlled_pauli_gates = ["cx", "cy", "cz"]
    hadamard_gate = ["h"]
    s_t_gates = ["s", "t", "sdg", "tdg"]

    if error_correction_code == "Q3Shor":
        supported_gates = (
            identity_gate
            + pauli_gates
            + controlled_pauli_gates
            + hadamard_gate
            + s_t_gates
        )
    elif error_correction_code == "Q5Laflamme":
        supported_gates = identity_gate + pauli_gates
    elif error_correction_code == "Q7Steane":
        supported_gates = (
            identity_gate
            + pauli_gates
            + controlled_pauli_gates
            + hadamard_gate
            + s_t_gates
        )
    elif error_correction_code == "Q9Shor":
        supported_gates = identity_gate + pauli_gates + controlled_pauli_gates
    elif error_correction_code == "Q9Surface":
        supported_gates = (
            identity_gate + pauli_gates + controlled_pauli_gates + hadamard_gate
        )
    elif error_correction_code == "Q18Surface":
        supported_gates = identity_gate + pauli_gates + hadamard_gate
    else:
        return (
            "error correction code: "
            + error_correction_code
            + " not supported. Check the OpenAPI spec to get a list of all currently supported error correction codes"
        )
    print(supported_gates)

    transpiled_circuits = [
        transpile(circuit, basis_gates=supported_gates) for circuit in circuits
    ]
    return transpiled_circuits
