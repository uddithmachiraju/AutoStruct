def extract_json_block(text: str) -> str:
    """
    Extracts and returns the JSON string from a markdown-style code block.
    Removes surrounding triple backticks and language hints (like ```json).
    """
    lines = text.strip().splitlines()
    # Remove lines that are just ``` or ```json etc.
    stripped_lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(stripped_lines).strip()