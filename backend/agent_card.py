import json
from llm import get_llm
from langchain_core.messages import HumanMessage

def generate_agent_card(business_map: dict, url: str) -> dict:
    biz_name = business_map.get("what_the_business_is", {}).get("value", "this business")
    provider_name = url.split("//")[-1].split("/")[0].replace("www.", "").split(".")[0].capitalize()

    prompt = f"""You are generating an A2A and MCP-compatible Agent Card for a business website.
    This card is consumed by OTHER AI agents that want to interact with this business.
    Generate it ONLY from the Business Map below. Do not add anything not proven by evidence.

    BUSINESS MAP:
    {json.dumps(business_map, indent=2)}

    FIELD INSTRUCTIONS — follow these exactly:

    name: Format as "<Provider> <Role> Agent". Example: "Sweetgreen Ordering Agent" or "Sweetgreen Restaurant Agent". Must describe what the agent DOES, not just the company name.

    description: Write a helpful one-sentence description for another AI agent reading this card. Format: "Your AI interface for [doing X, Y, Z] at [Business Name]." Example: "Your AI interface for browsing the menu, placing orders, and finding locations at Sweetgreen."

    provider.name: The real company name e.g. "Sweetgreen"
    provider.organization: The company domain e.g. "{url}"
    provider.type: The business category e.g. "Restaurant Chain", "SaaS", "Law Firm"

    capabilities.available_tools: List any detected MCP tools or APIs. Empty array [] if none found.
    capabilities.streaming: false
    capabilities.mcp_compatible: false unless evidence shows existing MCP
    capabilities.estimated_mcp_complexity: "low" (1-3 actions), "medium" (4-7), "high" (8+)

    skills: Each skill must represent one real action a customer or agent can take.
    - id: snake_case verb e.g. "browse_menu", "place_order", "find_location"
    - name: Human readable e.g. "Browse Menu", "Place Order"
    - description: What the skill does in plain English
    - how_to_invoke: The actual URL to navigate to, not markdown link text
    - input: Object with parameter names as keys and descriptions as values. Empty object if none needed.
    - output: Object with what the agent gets back. Empty object if unknown.
    - requires_auth: true/false based on evidence
    - evidence: A single URL string from the business map

    mcp_readiness:
    - has_existing_mcp: false unless proven
    - has_public_api: "yes"/"no"/"unknown"
    - detected_integrations: list of third party tools found e.g. ["shopify", "stripe"]
    - recommended_mcp_tools: List of snake_case tool function names that SHOULD be built for this business e.g. ["get_menu", "place_order", "find_location", "get_gift_card"]. Think about what an AI assistant would need to fully serve a customer of this business.
    - what_is_missing_to_build_mcp: Specific technical gaps e.g. ["no public ordering API", "auth flow unknown", "no webhook support found"]

    data_gaps: List fields that could not be confirmed from evidence
    confidence_score: 0.0 to 1.0 based on how much was proven vs unknown

    Return ONLY valid JSON, no markdown, no explanation:
    {{
    "schema_version": "1.0",
    "name": "...",
    "description": "...",
    "url": "{url}",
    "provider": {{
        "name": "...",
        "organization": "...",
        "type": "..."
    }},
    "capabilities": {{
        "available_tools": [],
        "streaming": false,
        "mcp_compatible": false,
        "estimated_mcp_complexity": "..."
    }},
    "skills": [
        {{
        "id": "...",
        "name": "...",
        "description": "...",
        "how_to_invoke": "...",
        "input": {{}},
        "output": {{}},
        "requires_auth": false,
        "evidence": "..."
        }}
    ],
    "mcp_readiness": {{
        "has_existing_mcp": false,
        "has_public_api": "...",
        "detected_integrations": [],
        "recommended_mcp_tools": [],
        "what_is_missing_to_build_mcp": []
    }},
    "contact_channels": {{}},
    "data_gaps": [],
    "confidence_score": 0.0
    }}"""

    llm = get_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = resp.content.strip()

    if "```" in raw:
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    start = raw.find("{")
    end = raw.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError(f"No JSON found: {raw[:200]}")
    raw = raw[start:end]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        open_braces = raw.count("{") - raw.count("}")
        open_brackets = raw.count("[") - raw.count("]")
        raw += "]" * open_brackets + "}" * open_braces
        return json.loads(raw)