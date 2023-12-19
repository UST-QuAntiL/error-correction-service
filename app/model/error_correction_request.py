import marshmallow as ma
from marshmallow import fields, ValidationError

class CircuitField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, list):
            return value
        else:
            raise ValidationError("Field should be str or list")

class ApplyECCRequest:
    def __init__(
        self,
        circuit,
        errorCorrectionCode,
        eccFrequency=100,
        circuitFormat="openqasm2"
    ):
        self.circuit = circuit
        self.errorCorrectionCode = errorCorrectionCode
        self.eccFrequency = eccFrequency
        self.circuitFormat = circuitFormat


class ApplyECCRequestSchema(ma.Schema):
    circuit = CircuitField(required=True)
    errorCorrectionCode = ma.fields.Str(required=True)
    eccFrequency = ma.fields.Int(required=False)
    circuitFormat = ma.fields.Str(required=False)

