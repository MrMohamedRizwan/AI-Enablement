from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agents.model.AgentState import AgentState
from mcp_tools.file_tool import read_file
from mcp_tools.web_tool import web_search
import json
import os

async def it_agent(state: AgentState) -> AgentState:
    """
    IT Support Agent - Handles all IT-related queries.
    
    Tools:
    - ReadFile for internal IT docs
    - WebSearch for external sources
    
    Example FAQs:
    - How to set up VPN?
    - What software is approved for use?
    - How to request a new laptop?
    """
    
    if "messages" not in state or len(state["messages"]) == 0:
        raise ValueError("state['messages'] is empty. Add at least one HumanMessage.")
    
    # Extract last user message
    last_user_message = next(
        (msg.content for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)),
        None
    )
    
    if last_user_message is None:
        raise ValueError("No HumanMessage found in state['messages']")

    print("🔧 IT Agent initiated...")

    # Initialize Azure OpenAI LLM with tools
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # your Azure deployment name
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
        ).bind_tools([read_file, web_search])

    system_prompt = """
    You are an IT Support Agent for the company.
    
    Your responsibilities:
    - Answer IT-related questions about technology, systems, software, hardware, VPN, laptops, access, and tools
    - Use the read_file tool to access internal IT documentation when relevant
    - Use the web_search tool to find additional information from external sources when needed
    - Provide clear, helpful, and accurate responses
    
    When using read_file, use domain "it" and specify the appropriate filename.
    
    Common IT topics you handle:
    - VPN setup and troubleshooting
    - Software approval and installation
    - Hardware requests (laptops, monitors, etc.)
    - System access and permissions
    - Network connectivity issues
    - Security protocols and best practices
    
    Always be helpful and provide step-by-step instructions when appropriate.
    """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=last_user_message),
    ]

    try:
        # Invoke the LLM
        response = await llm.ainvoke(messages)
        
        # Handle tool calls if present
        if hasattr(response, 'tool_calls') and response.tool_calls:
            print(f"🔧 IT Agent making {len(response.tool_calls)} tool call(s)...")
            
            # Process each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call['name']
                tool_args = tool_call['args']
                
                if tool_name == 'read_file':
                    # Ensure IT domain
                    if isinstance(tool_args, dict):
                        tool_args['domain'] = 'it'
                        tool_result = read_file.invoke(json.dumps(tool_args))
                    else:
                        tool_result = read_file.invoke(tool_args)
                elif tool_name == 'web_search':
                    if isinstance(tool_args, dict):
                        query = tool_args.get('query', str(tool_args))
                    else:
                        query = str(tool_args)
                    tool_result = web_search.invoke(query)
                else:
                    tool_result = f"Unknown tool: {tool_name}"
                
                print(f"🔧 Tool {tool_name} result: {tool_result[:100]}...")
            
            # Make a follow-up call with tool results
            messages.append(response)
            messages.append(HumanMessage(content=f"Tool results: {tool_result}"))
            final_response = await llm.ainvoke(messages)
            response_content = final_response.content
        else:
            response_content = response.content

        # Update state
        state["response"] = response_content
        state["llm_calls"] += 1
        state["messages"].append(AIMessage(content=response_content))

        print(f"🔧 IT Agent completed. Response: {response_content[:100]}...")
        return state

    except Exception as e:
        error_msg = f"IT Agent error: {str(e)}"
        print(f"❌ {error_msg}")
        state["response"] = error_msg
        state["messages"].append(AIMessage(content=error_msg))
        return state
