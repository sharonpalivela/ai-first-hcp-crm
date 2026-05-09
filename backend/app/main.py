from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, Base, SessionLocal
from app.models import Interaction
from app.schemas import ChatRequest, ChatResponse
from app.agent import agent

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI First HCP CRM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI First CRM Backend Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/agent/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):
    result = agent.invoke({
        "message": request.message,
        "current_draft": request.current_draft or {},
        "tool_used": "",
        "assistant_response": "",
        "updated_draft": {},
    })

    return {
        "assistant_response": result["assistant_response"],
        "tool_used": result["tool_used"],
        "updated_draft": result["updated_draft"],
    }


@app.post("/interaction/save")
def save_interaction(data: dict):
    db = SessionLocal()

    interaction = Interaction(
        hcp_name=data.get("hcp_name"),
        interaction_type=data.get("interaction_type"),
        products_discussed=data.get("products_discussed"),
        materials_shared=data.get("materials_shared"),
        samples_distributed=data.get("samples_distributed"),
        sentiment=data.get("sentiment"),
        follow_up_action=data.get("follow_up_action"),
        summary=data.get("summary"),
        compliance_risk=data.get("compliance_risk"),
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    db.close()

    return {
        "message": "Interaction saved successfully",
        "interaction_id": interaction.id,
    }