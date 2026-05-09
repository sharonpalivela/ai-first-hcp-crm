import os
import re
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
)


class AgentState(TypedDict):
    message: str
    current_draft: dict
    tool_used: str
    assistant_response: str
    updated_draft: dict


def extract_hcp_name(text: str):
    doctor_match = re.search(r"dr\.?\s+([a-zA-Z]+)", text, re.IGNORECASE)

    if doctor_match:
        return f"Dr. {doctor_match.group(1)}"

    return None


def ai_agent_node(state: AgentState):
    message = state["message"]
    lower_message = message.lower()

    current_draft = state.get("current_draft", {})
    updated_draft = current_draft.copy()

    extracted_hcp_name = extract_hcp_name(message)

    if (
        "change" in lower_message
        or "actually" in lower_message
        or "sorry" in lower_message
        or "not" in lower_message
    ):
        tool_used = "edit_interaction"

        if "negative" in lower_message:
            updated_draft["sentiment"] = "negative"
        elif "positive" in lower_message:
            updated_draft["sentiment"] = "positive"
        elif "neutral" in lower_message:
            updated_draft["sentiment"] = "neutral"

        assistant_response = (
            "Updated the interaction draft while keeping other fields unchanged."
        )

    elif "profile" in lower_message or "history" in lower_message:
        tool_used = "hcp_profile_lookup"

        hcp_name = extracted_hcp_name or updated_draft.get("hcp_name") or "Selected HCP"

        updated_draft["hcp_profile"] = {
            "hcp_name": hcp_name,
            "specialty": "Cardiology",
            "preferred_channel": "In-person meetings",
            "last_interaction": "Discussed efficacy and safety profile",
        }

        assistant_response = "Retrieved HCP profile and historical interaction details."

    elif "next step" in lower_message or "suggest" in lower_message:
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

        if "cardiox" in lower_message:
            updated_draft["products_discussed"] = "CardioX"

        if "brochure" in lower_message:
            updated_draft["materials_shared"] = "Product brochure"

        if "2 samples" in lower_message:
            updated_draft["samples_distributed"] = "2 samples"

        if "positive" in lower_message:
            updated_draft["sentiment"] = "positive"
        elif "negative" in lower_message:
            updated_draft["sentiment"] = "negative"
        elif "neutral" in lower_message:
            updated_draft["sentiment"] = "neutral"

        if "follow up" in lower_message:
            updated_draft["follow_up_action"] = "Follow up with HCP next Tuesday"

        llm_response = llm.invoke(
            [
                HumanMessage(
                    content=f"""
Summarize this pharma sales representative interaction professionally and concisely:

{message}
"""
                )
            ]
        )

        updated_draft["summary"] = llm_response.content
        assistant_response = (
            "Interaction logged and structured CRM fields populated successfully."
        )

    risky_words = ["cure", "100% effective", "no side effects", "guaranteed"]

    compliance_risk = "low"
    compliance_message = "No compliance concerns detected."

    for word in risky_words:
        if word in lower_message:
            compliance_risk = "high"
            compliance_message = f"Potentially risky pharma claim detected: '{word}'"

    updated_draft["compliance_risk"] = compliance_risk
    updated_draft["compliance_message"] = compliance_message

    return {
        "tool_used": tool_used,
        "assistant_response": assistant_response,
        "updated_draft": updated_draft,
    }


graph = StateGraph(AgentState)
graph.add_node("ai_agent", ai_agent_node)
graph.set_entry_point("ai_agent")
graph.add_edge("ai_agent", END)

agent = graph.compile()