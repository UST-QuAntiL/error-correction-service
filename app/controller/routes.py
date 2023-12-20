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

from app import error_correction_service
from flask_smorest import Blueprint
from app.model.error_correction_request import (
    ApplyECCRequest,
    ApplyECCRequestSchema,
)
from app.model.error_correction_response import (
    ApplyECCResponse,
    ApplyECCResponseSchema,
)

blp = Blueprint(
    "error-correction",
    __name__,
    description="Error Correction for quantum circuits",
)


@blp.route("/applyECC", methods=["POST"])
@blp.arguments(
    ApplyECCRequestSchema,
    example={
        "circuit": 'OPENQASM 2.0;\ninclude "qelib1.inc";qreg q[2];\ncreg c[2];\nh q[0];\ncx q[0], q[1];\n',
        "errorCorrectionCode": "Q7Steane",
        "eccFrequency": "20",
    },
    description="Q3Shor, Q5Laflamme, Q7Steane, Q9Shor, Q9Surface, and Q18Surface are currently supported ECC codes (Details here: https://mqt.readthedocs.io/projects/qecc/en/latest/EccFramework.html)",
)
@blp.response(200, ApplyECCResponseSchema)
def compute_corrected_circuit(json: dict):
    """Precompute classical MaxCut solution."""
    print("request", json)
    return error_correction_service.apply_ecc(ApplyECCRequest(**json))
