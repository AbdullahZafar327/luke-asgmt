import json
from llm import get_llm
from langchain_core.messages import HumanMessage

def generate_agent_card(business_map: dict, url: str) -> dict:
    prompt = f"""You are generating a machine-readable Agent Card.
This card will be used by AI agents to understand how to interact with a business.
Generate it from the Business Map below — not from assumptions.
BUSINESS MAP:
{json.dumps(business_map, indent=2)}
Design a useful Agent Card JSON structure yourself. It should include at minimum:
- agent_card_version
- business identity (name, type, description)
- base_url
- capabilities (what an agent CAN do with this business)
- available_actions (with endpoint or method if known, else "unknown")
- required_auth
- contact_channels
- tool_integrations (e.g. calendly, shopify detected)
- data_gaps (things marked unknown that an agent should know it can't rely on)
- confidence_score (0-1, how complete is this card based on evidence)
Return ONLY valid JSON. No markdown. No explanation."""

    llm = get_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = resp.content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)