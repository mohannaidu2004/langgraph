from langchain_community.llms import Ollama
from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any, List
import re
import json
import asyncio
from datetime import datetime

class AgentState(TypedDict):
    input: str
    next: str
    result: str
    route_history: List[str]
    timestamp: str
    context: Dict[str, Any]

llm = Ollama(model="mistral", temperature=0.3)

def log_node_execution(node_name: str, input_data: str, output: str) -> None:
    """Log node execution for debugging and monitoring"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Node '{node_name}' executed")
    print(f"  Input: {input_data[:100]}...")
    print(f"  Output: {output[:100]}...")
    print("-" * 50)

def router_node(state: AgentState) -> AgentState:
    """
    Router node that analyzes input and determines which specialized node to route to.
    Routes based on content analysis and pattern matching.
    """
    prompt = state["input"].lower()
    
    if "route_history" not in state:
        state["route_history"] = []
    
    if any(keyword in prompt for keyword in ["summarize", "summary", "brief", "explain", "describe"]):
        next_node = "summarizer"
    elif any(op in prompt for op in ["+", "-", "*", "/", "calculate", "solve", "math", "equation"]):
        next_node = "math"
    elif any(keyword in prompt for keyword in ["translate", "translate to", "in french", "in spanish", "in german"]):
        next_node = "translator"
    else:
        next_node = "fallback"
    
    state["route_history"].append(f"router -> {next_node}")
    state["next"] = next_node
    state["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_node_execution("router", state["input"], f"Routing to: {next_node}")
    
    return state

def math_node(state: AgentState) -> AgentState:
    """
    Math solver node that handles mathematical queries and calculations.
    Uses the LLM to solve mathematical problems.
    """
    prompt = f"""
    You are a mathematical problem solver. Please solve the following math problem step by step.
    If it's a word problem, extract the mathematical components first.
    
    Problem: {state['input']}
    
    Provide a clear, step-by-step solution with the final answer.
    """
    
    try:
        response = llm.invoke(prompt)
        result = f"Mathematical Solution:\n{response}"
        state["result"] = result
        state["next"] = "final"
        state["route_history"].append("math -> final")
        
        log_node_execution("math", state["input"], result)
        
    except Exception as e:
        state["result"] = f"Error in math processing: {str(e)}"
        state["next"] = "final"
    
    return state

def summary_node(state: AgentState) -> AgentState:
    """
    Text summarizer node that processes text summarization and explanation requests.
    """
    content = state["input"]
    if "summarize" in content.lower():
        content = re.sub(r'summarize:?|summary:?', '', content, flags=re.IGNORECASE).strip()
    
    prompt = f"""
    Please provide a clear and concise summary of the following text or topic.
    If it's a topic, provide a brief explanation with key points.
    
    Content: {content}
    
    Provide a well-structured summary with the main points.
    """
    
    try:
        response = llm.invoke(prompt)
        result = f"Summary:\n{response}"
        state["result"] = result
        state["next"] = "final"
        state["route_history"].append("summarizer -> final")
        
        log_node_execution("summarizer", state["input"], result)
        
    except Exception as e:
        state["result"] = f"Error in summarization: {str(e)}"
        state["next"] = "final"
    
    return state

def translator_node(state: AgentState) -> AgentState:
    """
    Translator node that handles language translation requests.
    """
    prompt = f"""
    You are a language translator. Please translate the following text based on the request.
    If the target language is not specified, try to infer from the context.
    
    Translation request: {state['input']}
    
    Provide the translation with the source and target language identified.
    """
    
    try:
        response = llm.invoke(prompt)
        result = f"Translation:\n{response}"
        state["result"] = result
        state["next"] = "final"
        state["route_history"].append("translator -> final")
        
        log_node_execution("translator", state["input"], result)
        
    except Exception as e:
        state["result"] = f"Error in translation: {str(e)}"
        state["next"] = "final"
    
    return state

def fallback_node(state: AgentState) -> AgentState:
    """
    Fallback node for general queries that don't match specific categories.
    Provides general conversational responses.
    """
    prompt = f"""
    You are a helpful assistant. Please provide a thoughtful response to the following query:
    
    Query: {state['input']}
    
    Provide a helpful and informative response.
    """
    
    try:
        response = llm.invoke(prompt)
        result = f"General Response:\n{response}"
        state["result"] = result
        state["next"] = "final"
        state["route_history"].append("fallback -> final")
        
        log_node_execution("fallback", state["input"], result)
        
    except Exception as e:
        state["result"] = f"Error in general processing: {str(e)}"
        state["next"] = "final"
    
    return state

def final_node(state: AgentState) -> AgentState:
    """
    Final processor node that formats and outputs the final result.
    Also provides routing history for transparency.
    """
    result = state.get("result", "No result generated")
    route_history = state.get("route_history", [])
    timestamp = state.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    final_output = f"""
{'='*50}
LANGGRAPH AGENT RESPONSE
{'='*50}

Original Query: {state['input']}
Processed at: {timestamp}
Route History: {' → '.join(route_history)}

{result}

{'='*50}
"""
    
    state["result"] = final_output
    state["next"] = END
    
    log_node_execution("final", "Processing complete", "Final output generated")
    
    return state

def determine_next_node(state: AgentState) -> str:
    """
    Routing function that determines the next node based on the current state.
    This is used by LangGraph to determine edge routing.
    """
    return state.get("next", "fallback")

# Create the graph
def create_agent_graph():
    """
    Create and configure the LangGraph agent with all nodes and edges.
    """
    graph = StateGraph(AgentState)
    
    graph.add_node("router", router_node)
    graph.add_node("math", math_node)
    graph.add_node("summarizer", summary_node)
    graph.add_node("translator", translator_node)
    graph.add_node("fallback", fallback_node)
    graph.add_node("final", final_node)
    
    graph.set_entry_point("router")
    
    graph.add_conditional_edges(
        "router",
        determine_next_node,
        {
            "math": "math",
            "summarizer": "summarizer",
            "translator": "translator",
            "fallback": "fallback"
        }
    )
    
    graph.add_edge("math", "final")
    graph.add_edge("summarizer", "final")
    graph.add_edge("translator", "translator")
    graph.add_edge("fallback", "final")
    
    return graph.compile()

def test_agent_with_examples():

    #Test the agent with various example inputs to demonstrate routing.

    app = create_agent_graph()
    
    test_cases = [
        "Calculate 15 + 25 * 3",
        "Summarize: LangGraph is a powerful orchestration framework for building multi-agent systems with LLMs.",
        "Translate 'Hello, how are you?' to French",
        "What is the capital of France?"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n TEST CASE {i}")
        print(f"Input: {test_input}")
        
        try:
            result = app.invoke({"input": test_input})
            print(result["result"])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting LangGraph Agent with Mistral via Ollama")
    print("=" * 50)
    
    app = create_agent_graph()
    
    test_agent_with_examples()
    
    print("\n Interactive Mode - Enter your queries (type 'quit' to exit):")
    
    
    while True:
        user_input = input("\n Query: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print(" Goodbye!")
            break
        
        if user_input:
            try:
                result = app.invoke({"input": user_input})
                print(result["result"])
            except Exception as e:
                print(f" Error: {e}")
        else:
            print("Please enter a query or 'quit' to exit.")