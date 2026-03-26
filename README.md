# 📰 JOVEMPANO (Versão Essencial)

**JOVEMPANO** é uma plataforma minimalista de curadoria e criação de notícias. Refatorada para focar no que importa: estabilidade extrema, manutenção limpa e escrita manual livre sob a arquitetura SQLite local.

## 🚀 Arquitetura (Modo KISS)

O projeto foi podado sob o princípio *Keep It Simple, Stupid*, eliminando dependências paralisantes (bancos de dados em nuvem via Docker, workers assíncronos) e resultando nesta infraestrutura perfeitamente enxuta:

1. **/backend**: O Motor (Python + FastAPI).
   - CRUD simplório para postagem e leitura de matérias.
   - Ponto de Segurança com **JWT** protegendo a criação (`/admin`).
   - Banco de Dados de arquivo único em **SQLite**.
2. **/frontend**: A Vitrine (Node.js + Vue 3).
   - Single Page App (SPA) desenhada com Vite/Tailwind.
   - **`/admin`**: Painel protegido para administradores digitarem com foco e postarem as notícias.
   - **`/`**: Feed belo estilizado para leitura veloz, livre de distrações javascript.

## ⚙️ Como Executar e Trabalhar

**1. Levantando o Backend**
```bash
cd backend
python -m venv venv
# ative o venv (Windows: venv\Scripts\activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```
A API desperta na porta `:8000`. (*Dica: O superusuário nasce na primeira linha com as credenciais padrão de ambiente: usuário: admin, senha: admin*).

**2. Levantando o Frontend**
```bash
cd frontend
npm install
npm run dev
```
Navegue logo para `http://localhost:5173`. O motor estelar e limpo do JOVEMPANO estará operante.
