from langchain.agents import AgentState

class ElasticBookState(AgentState):
    title: str | None
    author: str | None
    year: int | None