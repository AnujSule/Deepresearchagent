from langgraph.graph import StateGraph, END 
from langgraph.graph.message import add_messages 
from dotenv import load_dotenv 
from agents.research_agent import create_research_agent
from agents.answer_drafter_agent import generate_answer
from typing import TypedDict

load_dotenv()

# Step 1: Define our basic shared state
class GraphState(TypedDict):
    query: str
    context: str
    final_answer: str

# Step 2: Define our nodes

# Research node: performs the web search using Tavily
def research_node(state: GraphState) -> GraphState:
    query = state["query"]
    search_tool = create_research_agent()
    results = search_tool.run(query)
    state["context"] = results
    return state

# Answer node: generates a summary using Hugging Face
def answer_node(state: GraphState) -> GraphState:
    context = state["context"]
    answer = generate_answer(context)   #answer = generate_answer(context, state["query"]) use this for QA type
    state["final_answer"] = answer
    return state

# Step 3: Define the LangGraph workflow
workflow = StateGraph(GraphState)
workflow.add_node("research", research_node)
workflow.add_node("answer", answer_node)

workflow.set_entry_point("research")
workflow.add_edge("research", "answer")
workflow.add_edge("answer", END)

app = workflow.compile()

# Step 4: Run it
if __name__ == "__main__":
    user_query = input("Ask your research question: ")
    result = app.invoke({"query": user_query})
    print("\n📄 Final Answer:\n", result["final_answer"])