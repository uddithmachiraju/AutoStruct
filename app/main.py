import os 
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from core.schema.schema_loader import SchemaValidator
from core.preprocessing.file_preprocessor import FilePreprocessor

app = FastAPI()

class ExtractionRequest(BaseModel):
    text: str
    schema: dict 

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    preprocessor = FilePreprocessor()
    text, metadata = preprocessor.read(temp_path)
    os.remove(temp_path)
    return {"text": text, "metadata": metadata} 

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