# Análise do Erro 400 (BadRequestError)

## O Erro
```
openai.BadRequestError: Error code: 400 - Invalid parameter: messages with role 'tool' must be a response to a preceeding message with 'tool_calls'.
```

## A Causa
O erro ocorre porque há uma **inconsistência no histórico da conversa** enviado para a OpenAI.

1.  **Mensagem do Assistente (Assistant)**: O assistente gerou uma chamada de ferramenta com um ID específico (ex: `call_AzWhi...`). Esta mensagem foi salva corretamente na memória.
2.  **Mensagem da Ferramenta (Tool)**: Quando o resultado da ferramenta foi enviado (via `/tools/result`), o `tool_call_id` não foi fornecido ou foi salvo como `None`.
3.  **Formatação da Memória**: Ao reconstruir o histórico para enviar à OpenAI (`ConversationMemory`), o sistema converteu o `tool_call_id` nulo para `"unknown"`.

## O Resultado
A OpenAI recebe:
*   **Assistant**: "Chame a tool com ID `call_AzWhi...`"
*   **Tool**: "Aqui está o resultado para a tool com ID `unknown`"

Como os IDs não batem (`call_AzWhi...` != `unknown`), a OpenAI rejeita a requisição, pois não consegue vincular a resposta da ferramenta à chamada original.

## Por que aconteceu?
Isso aconteceu porque uma tentativa anterior de enviar o resultado da ferramenta falhou em fornecer o ID, e o sistema (antes da correção aplicada no passo anterior) salvou o registro incompleto na memória.

## Solução
Como o armazenamento atual é **em memória (in-memory)**, a solução imediata para limpar o estado inconsistente é:

1.  **Reiniciar o servidor** (`app.py`). Isso limpará o histórico corrompido.
2.  A correção já aplicada no `ToolResultService` (que infere o ID automaticamente se ele não for enviado) prevenirá que isso aconteça novamente em novas conversas.
