import pytest 
from core.schema.schema_loader import SchemaValidator 

def test_valid_candidate():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    validator = SchemaValidator(schema)
    
    data = {"name": "John Doe"}
    is_valid, error_message = validator.validate_data(data)
    
    assert is_valid is True
    assert error_message is None 

def test_invalid_candidate():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    validator = SchemaValidator(schema)
    
    data = {"name": 123}  # Invalid because name should be a string
    is_valid, error_message = validator.validate_data(data)
    
    assert is_valid is False
    assert error_message is not None
    assert "123 is not of type 'string'" in error_message