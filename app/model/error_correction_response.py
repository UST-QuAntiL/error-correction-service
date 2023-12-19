import marshmallow as ma
from marshmallow import fields, ValidationError

class CircuitField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str) or isinstance(value, list):
            return value
        else:
            raise ValidationError("Field should be str or list")

class ApplyECCResponse:
    def __init__(self, circuit, circuit_depth, circuit_width, list_input):
        super().__init__()
        self.circuit = circuit.qasm() if list_input else circuit[0].qasm()
        self.circuit_depth = circuit_depth if list_input else circuit_depth[0]
        self.circuit_width = circuit_width if list_input else circuit_width[0]

    def to_json(self):
        json_apply_ecc_response = {
            "circuit": self.circuit,
            "circuit_depth": self.circuit_depth,
            "circuit_width": self.circuit_width,
        }
        return json_apply_ecc_response


class ApplyECCResponseSchema(ma.Schema):
    circuit = CircuitField()
    circuit_depth = ma.fields.Int()
    circuit_width = ma.fields.Int()


