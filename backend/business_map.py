import json
from llm import get_llm
from langchain_core.messages import HumanMessage

def generate_business_map(extracted: dict) -> dict:
    prompt = f"""You are analyzing a business website. Based ONLY on the evidence below, fill out this Business Map.
RULES:
- If something is NOT proven by the evidence, mark it as "unknown"
- Every claim needs a source_evidence field (quote or URL)
- Do NOT hallucinate or infer beyond what the text shows
EVIDENCE:
Pages found: {extracted['pages_found']}
Forms: {json.dumps(extracted['forms'])}
Contact: {json.dumps(extracted['contact'])}
Third-party tools: {extracted['third_party_tools']}
Raw text sample: {extracted['raw_text_sample'][:1500]}
Return ONLY valid JSON in this exact structure:
{{
  "what_the_business_is": {{"value": "...", "evidence": "..."}},
  "products_or_services": [{{"name": "...", "evidence": "..."}}],
  "customer_actions_possible": [{{"action": "...", "how": "...", "evidence": "..."}}],
  "tools_and_forms": [{{"tool": "...", "purpose": "...", "evidence": "..."}}],
  "contact_info": {{"phone": "...", "email": "...", "address": "...", "evidence": "..."}},
  "payment_methods": {{"value": "...", "evidence": "..."}},
  "auth_required": {{"value": "...", "evidence": "..."}},
  "missing_or_unclear": ["..."],
  "pages_analyzed": {extracted['pages_found']}
}}"""

    llm = get_llm()
    resp = llm.invoke([HumanMessage(content=prompt)])
    raw = resp.content.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)