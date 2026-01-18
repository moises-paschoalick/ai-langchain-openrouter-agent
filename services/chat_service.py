from agents.chat_agent import get_chat_agent

agent_executor = get_chat_agent()

def process_prompt(prompt: str):
    response = agent_executor.invoke({"input": prompt})

    tools_usadas = []
    for step in response.get("intermediate_steps", []):
        action, result = step
        tools_usadas.append({
            "tool": action.tool,
            "input": action.tool_input,
            "output": result
        })

    return {
        "answer": response["output"],
        "tools_called": tools_usadas
    }
