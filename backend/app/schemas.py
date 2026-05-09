from pydantic import BaseModel
from typing import Optional


class InteractionCreate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    products_discussed: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    objections: Optional[str] = None
    follow_up_action: Optional[str] = None
    follow_up_date: Optional[str] = None
    summary: Optional[str] = None
    compliance_risk: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    current_draft: Optional[dict] = None


class ChatResponse(BaseModel):
    assistant_response: str
    tool_used: Optional[str] = None
    updated_draft: Optional[dict] = None