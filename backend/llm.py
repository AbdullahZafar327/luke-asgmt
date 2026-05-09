import os
from dotenv import load_dotenv
load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "claude"

def get_llm():
    if PROVIDER == "claude":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model="claude-sonnet-4-20250514",
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    else:
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            temperature=0.1,
            num_predict=4096, 
            num_ctx=8192       
        )