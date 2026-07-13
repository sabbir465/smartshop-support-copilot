from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse
from graph_agent import run_graph_agent
from data import CUSTOMERS, ORDERS
from policy import REFUND_POLICY
from demo_cases import DEMO_CASES

app = FastAPI(title="AI Refund Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/mock-data")
def mock_data():
    return {
        "customers": CUSTOMERS,
        "orders": ORDERS,
        "policy": REFUND_POLICY,
    }

@app.get("/demo-cases")
def demo_cases():
    return {"demo_cases": DEMO_CASES}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return run_graph_agent(request.message)