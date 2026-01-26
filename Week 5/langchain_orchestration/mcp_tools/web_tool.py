from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """
    Search the public web for general information.
    Input: a plain text query string.
    """
    print(f"\n[TOOL CALLED] WebSearch with query: {query}")
    return f"[WebSearch] Public info for: {query}"
