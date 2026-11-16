from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class BookSearchState(TypedDict):
    messages: Annotated[list, add_messages]
    title: str | None
    author: str | None
    year: int | None