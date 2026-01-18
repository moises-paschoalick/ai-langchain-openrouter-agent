from langchain.tools import tool
from datetime import datetime

@tool
def consultar_status_sistema(nome: str) -> str:
    """Consulta o status de um sistema interno pelo nome."""
    status = {
        "pagamentos": "Sistema de pagamentos está OPERACIONAL",
        "login": "Sistema de login está com INSTABILIDADE",
    }
    return status.get(nome.lower(), "Sistema não encontrado")

@tool
def obter_data_hora_atual() -> str:
    """Retorna a data e a hora atual do sistema no formato DD/MM/YYYY HH:MM:SS."""
    agora = datetime.now()
    return agora.strftime("%d/%m/%Y %H:%M:%S")