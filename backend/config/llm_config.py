import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0,
        default_headers={
            "HTTP-Referer": "https://localhost:3000",
            "X-Title": "LangChain OpenRouter App"
        }
    )