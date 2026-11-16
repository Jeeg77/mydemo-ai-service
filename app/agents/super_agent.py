from langchain.tools import ToolRuntime, tool
from langchain.messages import HumanMessage, ToolMessage
from langgraph.types import Command
from app.agents.mcp_book_agent import mcp_book_agent
from app.agents.elastic_book_agent import elastic_book_agent
from app.models.book_search_state import BookSearchState
from langchain.agents import create_agent
from app.models.llm import model

@tool
async def search_external_books(runtime: ToolRuntime) -> str:
    """Book agent searches for books based on specified criteria."""
    title = runtime.state["title"]
    author = runtime.state["author"]
    year = runtime.state["year"]

    mcp_agent = await mcp_book_agent()

    response = await mcp_agent.ainvoke({
        "messages": [
            HumanMessage(content=f"Find books with title {title}, author {author}, and year {year}")
        ]
    })
    return response['messages'][-1].content


@tool
async def search_internal_books(runtime: ToolRuntime) -> str:
    """Book agent searches for books based on specified criteria."""
    title = runtime.state["title"]
    author = runtime.state["author"]
    year = runtime.state["year"]

    print("\n========== SEARCH INTERNAL BOOKS ==========")
    print(f"Stato ricevuto: {runtime.state}")
    print(f"Titolo: {title}")
    print(f"Autore: {author}")
    print(f"Anno: {year}")

    elastic_agent = await elastic_book_agent()
  
    print(
        "ANNOTAZIONI SCHEMA AGENTE:",
        elastic_agent.builder.state_schema.__annotations__
    )

    print(
        "CAMPI SCHEMA AGENTE:",
        getattr(elastic_agent.builder.state_schema, "model_fields", None)
    )

    elastic_input = {
        "messages": [
            HumanMessage(content="Search the internal catalog.")
        ],
        "title": title,
        "author": author,
        "year": year
    }

    print("INPUT ELASTIC AGENT:", elastic_input)

    response = await elastic_agent.ainvoke(elastic_input)

    print("===========================================\n")

    return response['messages'][-1].content


@tool
def update_state(
    runtime: ToolRuntime,
    title: str | None = None,
    author: str | None = None,
    year: int | None = None
) -> Command:
    """Update the book search criteria.

    Use None for any criterion that the user has not specified
    or that should not limit the search.
    """
    return Command(
        update={
            "title": title,
            "author": author,
            "year": year,
            "messages": [
                ToolMessage(
                    content="Successfully updated state",
                    tool_call_id=runtime.tool_call_id
                )
            ]
        }
    )

async def super_agent():

    return create_agent(
        model=model,
        tools=[search_external_books, search_internal_books, update_state],
        state_schema=BookSearchState,
        system_prompt="""
        You are a book research assistant.

        First find all the information you need to update the state. When you have the information, update the state.
        Once that has completed and returned, you can search books in two different sources:

        - Internal catalog: books stored in Elasticsearch.
        - External catalog: books available through Open Library.

        Choose the appropriate tools based on the user's request.
        You can use both sources when useful.

        Combine the results and provide a clear answer,
        distinguishing internal and external books.
        """
    )



   