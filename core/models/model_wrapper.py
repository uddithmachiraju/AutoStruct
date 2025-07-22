import os 
import google.generativeai as genai

class ModelWrapper:
    def __init__(self, api_key: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key) 
        self.client = genai.GenerativeModel(model_name)

    def call_model(self, prompt: str) -> str:
        try:
            response = self.client.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling model: {e}")
            return None 