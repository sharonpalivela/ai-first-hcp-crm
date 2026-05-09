import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, Base, SessionLocal
from app.models import Interaction
from app.schemas import ChatRequest, ChatResponse

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


def extract_hcp_name(text: str):
    doctor_match = re.search(r"dr\.?\s+([a-zA-Z]+)", text, re.IGNORECASE)

    if doctor_match:
        return f"Dr. {doctor_match.group(1)}"

    return None


@app.post("/agent/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):

    original_message = request.message
    message = request.message.lower()

    current_draft = request.current_draft or {}
    updated_draft = current_draft.copy()

    extracted_hcp_name = extract_hcp_name(original_message)

    if (
        "change" in message
        or "actually" in message
        or "sorry" in message
        or "not" in message
    ):
        tool_used = "edit_interaction"

        if "negative" in message:
            updated_draft["sentiment"] = "negative"
        elif "positive" in message:
            updated_draft["sentiment"] = "positive"
        elif "neutral" in message:
            updated_draft["sentiment"] = "neutral"

        assistant_response = (
            "Updated the interaction draft while keeping other fields unchanged."
        )

    elif "profile" in message or "history" in message:
        tool_used = "hcp_profile_lookup"

        hcp_name = extracted_hcp_name or updated_draft.get("hcp_name") or "Selected HCP"

        updated_draft["hcp_name"] = hcp_name
        updated_draft["hcp_profile"] = {
            "hcp_name": hcp_name,
            "specialty": "Cardiology",
            "preferred_channel": "In-person meetings",
            "last_interaction": "Discussed efficacy and safety profile",
        }

        assistant_response = "Retrieved HCP profile and historical interaction details."

    elif "next step" in message or "suggest" in message:
        tool_used = "suggest_next_action"

        updated_draft["next_best_action"] = (
            "Schedule a follow-up meeting and share clinical safety study PDF."
        )

        assistant_response = "Generated AI-recommended next best action."

    else:
        tool_used = "log_interaction"

        if extracted_hcp_name:
            updated_draft["hcp_name"] = extracted_hcp_name

        updated_draft["interaction_type"] = "In-person Meeting"

        if "cardiox" in message:
            updated_draft["products_discussed"] = "CardioX"

        if "brochure" in message:
            updated_draft["materials_shared"] = "Product brochure"

        if "2 samples" in message:
            updated_draft["samples_distributed"] = "2 samples"

        if "positive" in message:
            updated_draft["sentiment"] = "positive"
        elif "negative" in message:
            updated_draft["sentiment"] = "negative"
        elif "neutral" in message:
            updated_draft["sentiment"] = "neutral"

        if "follow up" in message:
            updated_draft["follow_up_action"] = "Follow up with HCP next Tuesday"

        updated_draft["summary"] = (
            "Captured the HCP interaction, extracted key CRM fields, and prepared the draft for review."
        )

        assistant_response = (
            "Interaction logged and structured CRM fields populated successfully."
        )

    risky_words = ["cure", "100% effective", "no side effects", "guaranteed"]

    compliance_risk = "low"
    compliance_message = "No compliance concerns detected."

    for word in risky_words:
        if word in message:
            compliance_risk = "high"
            compliance_message = f"Potentially risky pharma claim detected: '{word}'"

    updated_draft["compliance_risk"] = compliance_risk
    updated_draft["compliance_message"] = compliance_message

    return {
        "assistant_response": assistant_response,
        "tool_used": tool_used,
        "updated_draft": updated_draft,
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