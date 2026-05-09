from langchain_core.tools import tool


@tool
def log_interaction(user_message: str):
    """
    Captures a new HCP interaction from natural language.
    """
    return {
        "tool": "log_interaction",
        "description": "Extracts and logs HCP interaction details from natural language."
    }


@tool
def edit_interaction(edit_request: str):
    """
    Edits an existing interaction draft while preserving unchanged fields.
    """
    return {
        "tool": "edit_interaction",
        "description": "Updates only requested fields in the current interaction draft."
    }


@tool
def hcp_profile_lookup(hcp_name: str):
    """
    Looks up HCP profile details.
    """
    return {
        "tool": "hcp_profile_lookup",
        "hcp_name": hcp_name,
        "specialty": "Cardiology",
        "preferred_channel": "In-person meeting",
        "last_interaction": "Discussed product efficacy and safety profile"
    }


@tool
def suggest_next_action(context: str):
    """
    Suggests the next best sales action.
    """
    return {
        "tool": "suggest_next_action",
        "recommendation": "Follow up with clinical safety data and schedule a meeting next week."
    }


@tool
def compliance_check(statement: str):
    """
    Checks interaction content for risky or non-compliant pharmaceutical claims.
    """
    risky_words = ["cure", "guaranteed", "no side effects", "100% effective"]

    risk = "low"
    issue = "No major compliance concern detected."

    for word in risky_words:
        if word in statement.lower():
            risk = "high"
            issue = f"Potentially non-compliant claim detected: '{word}'"
            break

    return {
        "tool": "compliance_check",
        "risk_level": risk,
        "issue": issue
    }