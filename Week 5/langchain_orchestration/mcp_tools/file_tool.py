import json
from pathlib import Path
from langchain_core.tools import tool

@tool
def read_file(payload: str) -> str:
    """
    Read internal files.
    Input JSON:
    {
      "domain": "it" | "finance",
      "filename": "example.txt"
    }
    """
    print(f"\n[TOOL CALLED] ReadFile with payload: {payload}")
    data = json.loads(payload)
    domain = data["domain"]
    filename = data["filename"]

    path = Path("docs") / domain / filename
    if not path.exists():
        return "File not found"

    return path.read_text()
