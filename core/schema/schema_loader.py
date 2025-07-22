import jsonschema
from jsonschema import validate, ValidationError

class SchemaValidator:
    def __init__(self, schema: dict):
        self.schema = schema
        self.validator = jsonschema.Draft7Validator(schema) 

    def validate_data(self, data: dict):
        """Returns (True, None) if data is valid according to the schema, otherwise returns False and an error message."""
        try:
            self.validator.validate(data)
            return True, None 
        except ValidationError as e:
            return False, str(e) 