import json 
import re 
import os 
import tempfile 
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
from core.models.model_wrapper import ModelWrapper
from core.chunking.chunker import Chunker
from core.preprocessing.file_preprocessor import FilePreprocessor
from core.extraction.prompt_builder import PromptBuilder
from core.extraction.utils import extract_json_block 
from core.schema.schema_loader import SchemaValidator
from core.preprocessing.file_preprocessor import FilePreprocessor

app = FastAPI()

load_dotenv() 

@app.post("/extract")
async def extract(datafile: UploadFile = File(...), schemafile: UploadFile = File(...)):
    # --- 1. Save PDF and schema to temp files ---
    try:
        doc_ext = os.path.splitext(datafile.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=doc_ext) as tmp_doc:
            tmp_doc.write(await datafile.read())
            tmp_doc.flush()
        doc_file_path = tmp_doc.name

        schema_ext = os.path.splitext(schemafile.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=schema_ext) as tmp_schema:
            tmp_schema.write(await schemafile.read())
            tmp_schema.flush()
        schema_file_path = tmp_schema.name
    except Exception as e:
        return {"error": f"File handling error: {str(e)}"}

    # --- 2. Read and normalize PDF text ---
    preprocessor = FilePreprocessor()
    try:
        text, _ = preprocessor.read(doc_file_path)
    except Exception as e:
        os.unlink(doc_file_path)
        os.unlink(schema_file_path)
        return {"error": f"Failed to read document: {str(e)}"}
    os.unlink(doc_file_path)

    try:
        with open(schema_file_path, 'r', encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        os.unlink(schema_file_path)
        return {"error": f"Failed to read schema: {str(e)}"}
    os.unlink(schema_file_path)

    chucker = Chunker(max_length=10000) 
    prompt_builder = PromptBuilder(schema)
    model_adapter = ModelWrapper(api_key=os.getenv("GOOGLE_API_KEY"), model_name="gemini-2.0-flash")
    schema_validator = SchemaValidator(schema)

    chunks = chucker.chunk(text)
    model_outputs = []
    validation_errors = []

    print(f"Total chunks to process: {len(chunks)}") 
    for i, chunk in enumerate(chunks):
        prompt = prompt_builder.build_prompt(chunk)
        model_output = model_adapter.call_model(prompt)
        model_output = extract_json_block(model_output)
        # print(f"[DEBUG] model_output = {repr(model_output)}")
 
        try:
            candidate = json.loads(model_output)
            valid, validation_error = schema_validator.validate_data(candidate) 
        except Exception as e:
            candidate = {}
            valid = False
            validation_error = str(e)
        # print(candidate) 
        # print(valid, validation_error)

        model_outputs.append(model_output)
        if not valid:
            validation_errors.append({
                "chunk_index": i,
                "error": validation_error,
                "raw_output": model_output
            })

    parsed_outputs = []
    for raw in model_outputs:
        try:
            parsed_outputs.append(json.loads(raw))
        except json.JSONDecodeError as e:
            print(f"Error decoding: {e}")

    output_path = os.path.join(os.path.dirname(__file__), "..", "data", "output.json")
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(parsed_outputs, f, indent=2)

    print(f"Saved extracted data to: {output_path}")

    return {
        "total_chunks": len(chunks),
        "validation_errors": validation_errors,
    }