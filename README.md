# JOVEMPANO - Portal de Notícias Minimalista 🗞️

> **Minimalismo. Performance. Curadoria Humana.**

O **JOVEMPANO** abandonou a complexidade de automações por IA para se tornar uma plataforma de notícias essencial, focada na experiência do leitor e na agilidade do redator. Baseado no princípio **KISS (Keep It Simple, Stupid)**, o projeto utiliza uma arquitetura moderna que elimina containers pesados e dependências desnecessárias.

![Layout StormGamer](https://raw.githubusercontent.com/RafaHop3/JOVEMPANO/main/frontend/public/banner-demo.png) *(Imagem Ilustrativa)*

---

## ✨ Diferenciais (Arquitetura StormGamer)

- **Layout Split 70/30**: Grade de leitura focada (70%) com Sidebar informativa (30%) para máxima imersão.
- **Dark/Light Mode Nativo**: Alternância de tema instantânea com persistência de preferência.
- **SEO Dinâmico**: Integração com `@unhead/vue` para Meta Tags e OpenGraph perfeitos em cada notícia.
- **Painel Admin Blindado**: Área editorial protegida por JWT para publicações em tempo real.
- **Performance de Elite**: SPA construída com **Vue 3** e **Tailwind v4**, servida de forma ultraleve pelo Vite.
- **Backend Zero-Config**: Baseado em **FastAPI** e **SQLite**, pronto para rodar em qualquer VPS sem Docker.

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
| :--- | :--- |
| **Frontend** | Vue 3, Vite, Tailwind CSS v4, Vue Router |
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy |
| **Banco de Dados** | SQLite (Arquivo local `jovempano.db`) |
| **Segurança** | JWT (JSON Web Tokens), Bcrypt Hashing |
| **SEO** | @unhead/vue |

---

## 🚀 Como Rodar Localmente

### 1. Requisitos
- Python 3.10+
- Node.js 18+

### 2. Configuração do Motor (Backend)
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
A API estará disponível em `http://localhost:8000/docs`.

### 3. Configuração da Vitrine (Frontend)
Em outro terminal:
```bash
cd frontend
npm install
npm run dev
```
Acesse o portal em `http://localhost:5173`.

### 4. Credenciais Administrativas
Para acessar o painel editorial em `/admin`:
- **Usuário:** `admin`
- **Senha:** `admin` (ou configurada via `ADMIN_PASSWORD` no `.env`)

---

## 📄 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---
**Desenvolvido com foco em velocidade e simplicidade por Antigravity.**
