from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

@tool
def web_search(query: str) -> str:
    """
    Search the public web for general information.
    Input: a plain text query string.
    """
    print(f"\n[TOOL CALLED] WebSearch with query: {query}")
    ddg_search = DuckDuckGoSearchRun()
    result = ddg_search.run(query)
    return result
