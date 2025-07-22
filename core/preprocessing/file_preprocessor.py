import os 
from typing import Tuple 

class FilePreprocessor:
    def __init__(self):
        try:
            import pdfplumber
            self.pdfplumber = pdfplumber
        except ImportError:
            self.pdfplumber = None 
        try:
            import docx
            self.docx = docx
        except ImportError:
            self.docx = None

    def read(self, file_path: str) -> Tuple[str, dict]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf' and self.pdfplumber:
            return self.read_pdf(file_path)
        elif ext in ['.docx', '.doc'] and self.docx:
            return self.read_docx(file_path)
        elif ext in ['.txt', '.md']:
            return self.read_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
        
    def read_pdf(self, file_path: str) -> Tuple[str, dict]:
        text = ""
        with self.pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or "\n"
        return text, {} 
    
    def read_docx(self, file_path: str) -> Tuple[str, dict]:
        doc = self.docx.Document(file_path)
        text = "\n".join(paragraph.text for paragraph in doc.paragraphs)
        return text, {}
    
    def read_txt(self, file_path: str) -> Tuple[str, dict]:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text, {} 