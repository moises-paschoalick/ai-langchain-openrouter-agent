# openrouter-langchain-api

API REST em Python que utiliza **LangChain** integrado ao **OpenRouter** para executar agentes conversacionais com **LangChain Tools**, permitindo chamadas diretas de ferramentas durante a resposta do modelo.

O projeto foi criado com foco educacional e arquitetural, usando uma separação clara entre **routes**, **services**, **agents**, **tools** e **config**.

---

## Funcionalidades

- Integração com OpenRouter para uso de múltiplos LLMs
- Agente LangChain com suporte a **Tools**
- Tools customizadas (ex: status de sistemas, data e hora atual)
- Retorno informando **qual tool foi utilizada**
- API REST simples com Flask

---

## Estrutura do Projeto
```
├── app.py
├── routes/
│ └── chat_routes.py
├── services/
│ └── chat_service.py
├── agents/
│ └── chat_agent.py
├── tools/
│ └── system_tools.py
├── config/
│ └── llm_config.py
├── .env (arquivo não está no repositório veja o formato)
├── .gitignore
└── requirements.txt
```

## Configuração

### 1. Configurar variáveis de ambiente 
Criar o arquivo .env
```bash
OPENROUTER_API_KEY=sk*************3
```


### 2. Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências
```
pip install -r requirements.txt
```

### 4. Executando a aplicação
```
python app.py
```
A API estará disponível em:
http://localhost:5000

## Endpoint disponível
POST /chat
Processa um prompt usando o agente LangChain e retorna a resposta do modelo, incluindo a tool utilizada (quando aplicável).
```
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Qual o status do sistema de pagamentos?"
  }'
```
Response (exemplo)
```
{
  "answer": "Sistema de pagamentos está OPERACIONAL",
  "tool_used": "consultar_status_sistema"
}

```

---

## Considerações Finais

Este projeto demonstra como integrar **LangChain** com **OpenRouter** para criação de agentes conversacionais utilizando **Tools orquestradas**, expostas por meio de uma API REST.

A arquitetura modular facilita a adição de novas tools, modelos e regras de negócio, tornando-o adequado tanto para estudos quanto como base para projetos reais.

Contribuições, sugestões e evoluções são bem-vindas.

---

## Licença

Este projeto é disponibilizado para fins educacionais e de estudo.
