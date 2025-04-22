from langchain.tools import TavilySearchResults 
from langchain.agents import Tool
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

tavily_key = os.getenv("TAVILY_API_KEY")

def create_research_agent():
    tavily_tool = TavilySearchResults(api_key=tavily_key)

    search_tool = Tool(
        name="web_search",
        func=tavily_tool.run,
        description="Search the internet for up-to-date information"
    )

    return search_tool

if __name__ == "__main__":
    tool = create_research_agent()
    query = "Latest AI trends in 2025"
    result = tool.run(query)
    print("Search Results:\n", result)