# Docker Setup - LangChain OpenRouter

Este projeto agora está configurado para rodar com Docker usando **npm** (ao invés de yarn).

## 📦 Estrutura

- **Backend**: Flask API rodando na porta 5000
- **Frontend**: React + Vite servido com Nginx na porta 80

## 🚀 Como Usar

### Opção 1: Docker Compose (Recomendado)

Rode ambos os serviços (backend + frontend) com um único comando:

```bash
docker-compose up -d
```

Para parar:
```bash
docker-compose down
```

### Opção 2: Docker Individual

**Backend:**
```bash
cd backend
docker build -t langchain-backend .
docker run -d --name langchain-backend -p 5000:5000 --env-file .env langchain-backend
```

**Frontend:**
```bash
cd ..
docker build -f front-web/Dockerfile -t langchain-frontend .
docker run -d --name langchain-frontend -p 80:80 langchain-frontend
```

## 🔧 Configurações Importantes

### Backend (Flask)
- **Host**: `0.0.0.0` (permite conexões externas ao container)
- **Porta**: `5000`
- **Arquivo**: `backend/app.py`

### Frontend (Vite + React)
- **Build**: `npm run build` (gera pasta `dist/`)
- **Servidor**: Nginx
- **Porta**: `80`

## 📝 Arquivos Criados/Modificados

1. **backend/Dockerfile** - Container Python com Flask
2. **backend/.dockerignore** - Exclui arquivos desnecessários do build
3. **backend/app.py** - Atualizado para aceitar conexões externas
4. **front-web/Dockerfile** - Container Node + Nginx (usando npm)
5. **front-web/.dockerignore** - Exclui node_modules e arquivos desnecessários
6. **docker-compose.yml** - Orquestração dos serviços

## ✅ Testes Realizados

- ✅ Backend rodando na porta 5000
- ✅ Endpoint `/chat` respondendo corretamente
- ✅ Frontend buildando com npm (sem yarn)
- ✅ Frontend servindo com Nginx na porta 80

## 🔍 Troubleshooting

**Porta já em uso:**
```bash
# Parar containers existentes
docker-compose down
# ou
docker rm -f langchain-backend langchain-frontend

# Liberar porta manualmente
fuser -k 5000/tcp
```

**Rebuild após mudanças:**
```bash
docker-compose up -d --build
```

**Ver logs:**
```bash
docker-compose logs -f
# ou para um serviço específico
docker-compose logs -f backend
docker-compose logs -f frontend
```
