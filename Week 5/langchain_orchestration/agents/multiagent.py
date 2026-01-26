from agents.model.AgentState import AgentState
from typing import Literal
from langgraph.graph import StateGraph, END, START
from agents.finance_agent import finance_agent
from agents.it_agent import it_agent
from agents.supervisor import supervisor_agent

def route_to_agent(state: AgentState) -> Literal["IT","Finance"]:
    """
    Conditional edge function that determines which agent to invoke.
    """
    return state["route"]


def create_agent_graph():
    """
    Builds the LangGraph workflow with LLM-powered routing.
    """
    
    workflow = StateGraph(AgentState)
    
    # Add all nodes
    workflow.add_node("router", supervisor_agent)
    workflow.add_node("IT", it_agent)
    workflow.add_node("Finance", finance_agent)
    
    # Start with router
    workflow.add_edge(START, "router")
    
    # Conditional routing from router to agents
    workflow.add_conditional_edges(
        "router",
        route_to_agent,
        {
            "IT": "IT",
            "Finance": "Finance"        
        }
    )
    
    # All agents end the workflow
    workflow.add_edge("Finance", END)
    workflow.add_edge("IT", END)
    
    return workflow.compile()