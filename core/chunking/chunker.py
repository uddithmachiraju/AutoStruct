from typing import List 

class Chunker:
    def __init__(self, max_length: int = 4000):
        self.max_length = max_length

    def chunk(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = [] 
        count = 0 
        for word in words:
            count += len(word) + 1  # +1 for the space
            if count > self.max_length:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                count = len(word) + 1
            else:
                current_chunk.append(word)
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks 