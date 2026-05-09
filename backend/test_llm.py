from llm import get_llm
from langchain_core.messages import HumanMessage

llm = get_llm()
resp = llm.invoke([HumanMessage(content="Say hello and tell me what model you are in one sentence.")])
print(resp.content)