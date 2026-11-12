from langchain.tools import ToolRuntime, tool
from langchain.messages import HumanMessage, ToolMessage
from langgraph.types import Command
from app.agents.mcp_book_agent import book_agent
from app.models.book import Book
from langchain.agents import create_agent
from app.models.llm import model

@tool
async def search_external_books(runtime: ToolRuntime) -> str:
    """Book agent searches for books based on specified criteria."""
    title = runtime.state["title"]
    author = runtime.state["author"]
    year = runtime.state["year"]
    response = await book_agent.ainvoke({"messages": [HumanMessage(content=f"Find books with title {title}, author {author}, and year {year}")]})
    return response['messages'][-1].content

@tool
def update_state(title: str, author: str, year: str, runtime: ToolRuntime) -> str:
    """Update the state when you know all of the values: title, author, year.
    This tool must be called alone, without any other tool calls. It must complete and return to make,
    the information available to other tools."""
    return Command(update={
        "title": title,
        "author": author,
        "year": year,
        "messages": [ToolMessage("Successfully updated state", tool_call_id=runtime.tool_call_id)]}
        )

    
coordinator = create_agent(
    model=model,
    tools=[search_external_books, update_state],
    state_schema=Book,
    system_prompt="""
    You are a book coordinator. 
    First find all the information you need to update the state. When you have the information, update the state.
    Once that has completed and returned, you can delegate the tasks 
    to your specialists for recommendations.
    Once you have received their answers, coordinate the perfect book selection for me.
    """
)