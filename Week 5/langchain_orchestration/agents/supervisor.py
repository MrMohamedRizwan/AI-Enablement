from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from agents.model.AgentState import AgentState
from agents.model.RouteDecision import RouteDecision
import os 

async def supervisor_agent(state: AgentState) -> AgentState:
    """
    Supervisor router agent (Azure OpenAI).

    Purpose:
    - Classifies user queries into IT or Finance
    - Routes to the appropriate specialist agent
    """

    if "messages" not in state or len(state["messages"]) == 0:
        raise ValueError("state['messages'] is empty. Add at least one HumanMessage.")
    # Extract last user message
    last_user_message = next(
        (msg.content for msg in reversed(state["messages"]) if isinstance(msg, HumanMessage)),
        None
    )
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  # your Azure deployment name
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        temperature=0,
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY")
        ).with_structured_output(RouteDecision)

    if last_user_message is None:
        raise ValueError("No HumanMessage found in state['messages']")

    print("🧭 Routing agent initiated (Azure OpenAI)...")

    # Azure OpenAI LLM
    llm =llm
    system_prompt = """
        You are a Supervisor Agent responsible for routing employee queries
        to the correct specialist agent.

        Classify the user query into ONE category only.

        Categories:

        IT:
        - Technology, systems, software, hardware, VPN, laptops, access, tools

        Finance:
        - Payroll, reimbursement, expenses, invoices, budgets, payments

        Return ONLY the classification as structured output.
        """

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=last_user_message),
    ]

    # Invoke Azure OpenAI
    decision: RouteDecision = await llm.ainvoke(messages)

    # Update state
    state["route"] = decision.route
    state["llm_calls"] += 1
    state["messages"].append(
        SystemMessage(content=f"Router decision: {decision.route}")
    )

    print(f"🧭 ROUTER → Routing to: {decision.route}")
    return state
