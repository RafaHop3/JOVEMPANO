# JovemPano 🗞️

> **Minimalismo. Performance. Curadoria Humana.**

Portal de notícias moderno com painel editorial protegido por JWT, carrossel de banners destaque e feed de notícias com imagem de capa. Arquitetura Vue 3 + FastAPI + SQLite, sem Docker, pronto para rodar em qualquer VPS.

---

## ✨ Funcionalidades

| Feature | Descrição |
| :--- | :--- |
| 🖼️ **Banner Destaque** | Carrossel full-width com balão glassmorphism, auto-play e navegação por dots/setas |
| 📰 **Feed com Imagens** | Notícias com foto de capa, zoom no hover e expansão inline |
| 🌗 **Dark / Light Mode** | Alternância nativa com persistência de preferência |
| 🔒 **Admin Protegido** | Painel editorial em abas com autenticação JWT |
| 🛡️ **Gestão de Banners** | Criar, ativar/desativar e excluir banners sem sair do painel |
| ⚡ **Performance de Elite** | SPA Vue 3 + Vite, backend FastAPI + SQLite, zero overhead |

---

## 🛠️ Stack

| Camada | Tecnologia |
| :--- | :--- |
| **Frontend** | Vue 3, Vite, Tailwind CSS v4, Vue Router |
| **Backend** | Python 3.10+, FastAPI, SQLAlchemy, Pydantic v2 |
| **Banco de Dados** | SQLite (criado automaticamente na 1ª inicialização) |
| **Segurança** | JWT (HS256), Bcrypt |

---

## 🚀 Como Rodar Localmente

### Pré-requisitos
- Python 3.10+
- Node.js 18+

### 1. Backend

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

**Configurar variáveis de ambiente:**

```bash
# Copie o exemplo e edite com seus valores
cp .env.example .env
```

```env
# backend/.env
SECRET_KEY=troque-por-uma-chave-segura-e-longa
ADMIN_PASSWORD=troque-por-uma-senha-forte
DATABASE_URL=sqlite:///./jovempano.db
```

**Iniciar:**
```bash
uvicorn app.main:app --reload
```

A API e documentação estarão em `http://localhost:8000/docs`.

### 2. Frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Acesse o portal em `http://localhost:5173`.

> **Nota:** O banco de dados e o usuário `admin` são criados automaticamente na primeira inicialização do backend.

---

## 🖼️ Imagens de Exemplo

O projeto inclui 4 imagens geradas com IA prontas para usar no painel admin (disponíveis em `frontend/public/images/`):

| Arquivo | Uso sugerido |
| :--- | :--- |
| `hero_banner.png` | Fundo do banner destaque principal |
| `news_politica.png` | Imagem de capa para matérias de política |
| `news_economia.png` | Imagem de capa para matérias de economia |
| `news_esportes.png` | Imagem de capa para matérias de esportes |

---

## 🔑 Painel Administrativo

Acesse `/admin` no navegador. As credenciais são definidas via variáveis de ambiente (`.env`). **Não use as senhas padrão em produção.**

No painel você pode:
- **Aba Notícias** — Publicar matérias com título, imagem e corpo; excluir matérias existentes
- **Aba Banners Destaque** — Criar banners com preview em tempo real, ativar/desativar e excluir

---

## 📁 Estrutura do Projeto

```
JOVEMPANO/
├── backend/
│   ├── app/
│   │   ├── core/         # Segurança, configuração
│   │   ├── routers/      # Endpoints: news, banners, auth
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── schemas.py    # Pydantic schemas
│   │   └── main.py       # Entry point FastAPI
│   ├── .env.example
│   └── requirements.txt
└── frontend/
    ├── public/images/    # Imagens estáticas (capas, banners)
    └── src/
        ├── components/   # NewsCard, HeroBanner, SidebarWidget
        └── views/        # Home, Admin
```

---

## 📄 Licença

MIT — Distribuído sob a licença MIT.

---

*Desenvolvido com foco em velocidade e simplicidade.*
