from fastapi import FastAPI
from app.models.chat import ChatRequest
from app.agents.mcp_book_agent import create_book_agent
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.book_agent = await create_book_agent()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "UP"}


@app.post("/chat")
async def chat(request: ChatRequest):

    result = await app.state.book_agent.ainvoke({
        "messages": [
            {"role": "user", "content": request.message}
        ]
    })

    return result