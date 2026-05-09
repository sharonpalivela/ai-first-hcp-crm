import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.tools import (
    log_interaction,
    edit_interaction,
    hcp_profile_lookup,
    suggest_next_action,
    compliance_check
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

tools = [
    log_interaction,
    edit_interaction,
    hcp_profile_lookup,
    suggest_next_action,
    compliance_check
]

agent = create_react_agent(
    llm,
    tools
)