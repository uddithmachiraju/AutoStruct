from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class ExtractionRequest(BaseModel):
    text: str
    schema: dict 

@app.post("/extract")
async def extract(request: ExtractionRequest):
    return {
        "received_text": request.text,
        "received_schema": request.schema,
        "structured_data": {
            "example_key": "example_value"
        },
        "status": "under construction"
    }