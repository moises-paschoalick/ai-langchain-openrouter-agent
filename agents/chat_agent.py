from langchain.agents import AgentExecutor
from langchain.agents import create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.llm_config import get_llm
from tools.system_tools import (
    consultar_status_sistema, 
    obter_data_hora_atual
)

def get_chat_agent():
    llm = get_llm()
    

    tools = [
        consultar_status_sistema,
        obter_data_hora_atual
    ]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Você é um assistente técnico. "
            "Sempre informe explicitamente o nome da tool utilizada na resposta final."
        ),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        return_intermediate_steps=True
    )
