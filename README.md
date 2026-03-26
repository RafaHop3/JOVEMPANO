# 📰 JOVEMPANO

**JOVEMPANO** é uma plataforma automatizada e inteligente de curadoria e geração de notícias. Alimentada por Inteligência Artificial (LLMs) e técnicas avançadas de scraping (Spiders/RSS), construída no modelo Monorepo para separar o motor robusto da vitrine visual.

## 🚀 Arquitetura do Monorepo

O projeto está dividido nestas frentes principais:

1. **/backend**: O "Motor". Construído em **Python** (FastAPI).
   - Coleta de dados via RSS e Celery Workers.
   - Processamento de texto e integração estrita com LLMs (OpenAI via Structured Outputs).
   - Banco de Dados PostgreSQL (com SQLAlchemy Async).
2. **/frontend**: A "Vitrine". Construído em **Astro**.
   - SSG (Static Site Generation) para tempo de carregamento absoluto em milissegundos.
   - Desenho focado em legibilidade e tipografia (estilo Premium News).
   - Imune a quebras na borda, projetado para viver atrás do WAF da Cloudflare.

## 🛠️ Tecnologias Utilizadas
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Celery, Redis, PostgreSQL.
- **Frontend**: Astro, HTML/CSS (Vanilla Moderno).
- **IA**: OpenAI API (Garantia anti-alucinação por JSON Output).
- **Gerenciamento**: Git, monorepo, infraestrutura via Docker Compose na raiz.

## ⚙️ Como Executar Localmente

### 1. Subindo a infraestrutura (Banco e Fila)
Na raiz do projeto (`/JOVEMPANO`):
```bash
docker-compose up -d
```

### 2. Rodando o Backend (FastAPI + Celery)
```bash
cd backend
python -m venv venv
# Ative o venv (Windows: venv\Scripts\activate)
pip install -r requirements.txt
# Subir API
uvicorn app.main:app --reload
# Subir Worker (novo terminal)
celery -A app.worker.celery_app worker --loglevel=info -P solo
```

### 3. Rodando o Frontend (Astro)
```bash
cd frontend
npm install
npm run dev
```

## 🛡️ Políticas de Segurança e Contribuição
Visando as melhores práticas do fluxo GitFlow e Extreme Safety:
- **`main`**: Branch sagrada. Destinada apenas a código homologado e de produção. **Proibido commit direto.**
- **`dev`**: Branch base para sincronização do time.
- Toda contribuição nasce de divisões da `dev` com prefixos organizacionais (ex: `feature/nova_coleta`, `bugfix/erro_llm`).
- O `.gitignore` enraizado protege vazamentos de senhas e arquivos `.env`. Nunca faça bypass nessas regras de segurança.
