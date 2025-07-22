import json
from typing import Dict, Any, List 

class PromptBuilder:
    def __init__(self, schema: Dict[str, Any]):
        self.schema = schema

    def build_prompt(self, data: Dict[str, Any]) -> str:
        return f"""
            You are an AI assistant that extracts structured data from unstructured text.
            Follow the schema provided to extract the relevant information.
            Schema: {json.dumps(self.schema, indent=2)}
            Input Text: {data}

            RESPOND ONLY with a valid JSON object that matches the schema.
        """
