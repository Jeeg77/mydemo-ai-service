from fastapi import FastAPI
from app.models.chat import ChatRequest
from app.agents.super_agent import super_agent  
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.super_agent = await super_agent()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "UP"}


@app.post("/chat")
async def chat(request: ChatRequest):

    result = await app.state.super_agent.ainvoke({
        "messages": [
            {"role": "user", "content": request.message}
        ]
    })

    content = result["messages"][-1].content

    if isinstance(content, list):
        content = "\n".join(
            item["text"]
            for item in content
            if isinstance(item, dict) and item.get("type") == "text"
        )

    return {
        "response": content
    }