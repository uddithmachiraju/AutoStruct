import os 
import pytest 
from core.schema.schema_loader import SchemaValidator 
from core.preprocessing.file_preprocessor import FilePreprocessor
from core.chunking.chunker import Chunker 
from core.extraction.prompt_builder import PromptBuilder

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

def test_read_txt():
    test_txt = "Sample_text.txt"
    text_content = "This is a sample text file."
    with open(test_txt, 'w', encoding='utf-8') as f:
        f.write(text_content)

    preprocessor = FilePreprocessor()
    text, metadata = preprocessor.read(test_txt)
    os.remove(test_txt)
    assert text_content in text 

def test_read_pdf():
    test_pdf = "Sanjay_Uddith_Raju_Resume.pdf"

    if os.path.exists(test_pdf):
        preprocessor = FilePreprocessor()
        text, metadata = preprocessor.read(test_pdf)
        assert isinstance(text, str) 

def test_chunk_test():
    chunker  = Chunker(max_length = 20) 
    text = "This is a sample text that will be chunked into smaller parts."
    chunks = chunker.chunk(text)
    assert len(chunks) > 0
    assert isinstance(chunks, list)
    assert all(isinstance(chunk, str) for chunk in chunks) 

def test_build_prompt():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }
    pb = PromptBuilder(schema) 
    chunk = "My name is Sanjay Uddith Raju and I am a Machine Learning engineer."
    prompt = pb.build_prompt(chunk)
    assert "Schema:" in prompt and "Input Text" in prompt
    assert "Sanjay Uddith Raju" in prompt 