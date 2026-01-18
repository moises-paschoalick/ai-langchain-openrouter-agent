import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import ConversationBufferMemory
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Load environment variables
load_dotenv()

# Define a simple tool
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    if "sao paulo" in city.lower():
        return "Sunny, 25°C"
    elif "london" in city.lower():
        return "Cloudy, 15°C"
    else:
        return "Unknown weather"

def test_openrouter_memory_tools():
    print("--- Starting OpenRouter Test with Memory and Tools ---")

    # 1. Initialize ChatOpenAI with OpenRouter
    api_key = os.getenv("OPENROUTER_API_KEY")
    print(f"API Key loaded: {api_key[:10]}..." if api_key else "API Key NOT loaded")

    # 1. Initialize ChatOpenAI with OpenRouter
    llm = ChatOpenAI(
        model="openai/gpt-4o-mini",
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        temperature=0,
        default_headers={
            "HTTP-Referer": "https://localhost:3000", # Required by OpenRouter
            "X-Title": "LangChain OpenRouter Test"
        }
    )

    # 2. Setup Tools
    tools = [get_weather]

    # 3. Setup Prompt with Memory
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # 4. Setup Agent
    agent = create_openai_tools_agent(llm, tools, prompt)

    # 5. Setup Memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # 6. Setup Executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

    # 7. Run Conversation Sequence
    
    # Step A: Use a tool
    print("\n--- Step A: Asking about weather (Tool Usage) ---")
    response_a = agent_executor.invoke({"input": "What is the weather in Sao Paulo?"})
    print(f"Response A: {response_a['output']}")

    # Step B: Store in memory
    print("\n--- Step B: Providing info (Memory Storage) ---")
    response_b = agent_executor.invoke({"input": "My name is Moises."})
    print(f"Response B: {response_b['output']}")

    # Step C: Retrieve from memory
    print("\n--- Step C: Asking for info (Memory Retrieval) ---")
    response_c = agent_executor.invoke({"input": "What is my name?"})
    print(f"Response C: {response_c['output']}")

    print("\n--- Test Completed ---")

if __name__ == "__main__":
    test_openrouter_memory_tools()
