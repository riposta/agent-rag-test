from fastapi import FastAPI
from app.config import SCRAPE_URL, SCRAPE_INTERVAL, OPENAI_API_KEY
from app.webscraper import scrape_domain
from app.retriever import Retriever
from app.openai_agent import RAGAgentOpenAI
import time
import threading
import uvicorn

from model.model import AskRequest

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8050, reload=True)

app = FastAPI()
retriever = Retriever(OPENAI_API_KEY)
agent = RAGAgentOpenAI(retriever)

def update_knowledge_base():
    while True:
        text = scrape_domain(SCRAPE_URL)
        retriever.clear()
        retriever.add_documents([text])
        time.sleep(SCRAPE_INTERVAL)

@app.on_event("startup")
def startup_event():
    threading.Thread(target=update_knowledge_base, daemon=True).start()

@app.post("/ask")
async def ask(request: AskRequest):
    return {"answer": await agent(request.question)}

