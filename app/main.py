from fastapi import FastAPI 
from pydantic import BaseModel
from core.schema.schema_loader import SchemaValidator

app = FastAPI()

class ExtractionRequest(BaseModel):
    text: str
    schema: dict 

@app.post("/extract")
async def extract(request: ExtractionRequest):

    dummy_output = {
        "name": "Sanjay Uddith Raju"
    }

    schema_validator = SchemaValidator(request.schema)
    is_valid, error_message = schema_validator.validate_data(dummy_output)

    return {
        "received_text": request.text,
        "received_schema": request.schema,
        "structured_data": {dummy_output},
        "is_valid": is_valid,
        "error_message": error_message,
    } 