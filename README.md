# JovemPano 🗞️

> **Informação sem filtro, com a velocidade que o Brasil exige.**

Portal de notícias moderno com identidade visual azul & dourado, animação de fundo estilo água-viva, carrossel de banners destaque e navegação por categorias. Arquitetura Vue 3 + FastAPI + SQLite.

---

## ✨ Funcionalidades

| Feature | Descrição |
| :--- | :--- |
| 🖼️ **Banner Destaque** | Carrossel full-width com balão glassmorphism, auto-play e navegação por setas |
| 📰 **Feed com Imagens** | Notícias com foto de capa, zoom no hover e expansão inline |
| 🧭 **Navegação por Categorias** | 7 seções: Início, Política, Economia, Esportes, Tecnologia, Entretenimento, Mundo |
| 🪼 **Animação de Fundo** | Águas-vivas douradas pulsando suavemente em Canvas (quase invisível, elegante) |
| ✨ **Decorações Laterais** | Ornamentos geométricos dourados nas laterais em telas grandes |
| 🔒 **Admin Protegido** | Painel editorial em abas com autenticação JWT |
| 🛡️ **Gestão de Banners** | Criar, ativar/desativar e excluir banners sem sair do painel |

---

## 🛠️ Stack

| Camada | Tecnologia |
| :--- | :--- |
| **Frontend** | Vue 3, Vite, Tailwind CSS v4, Vue Router, Canvas API |
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
cp .env.example .env
# Edite o arquivo .env com seus valores
```

```env
SECRET_KEY=troque-por-uma-chave-segura-e-longa
ADMIN_PASSWORD=troque-por-uma-senha-forte
DATABASE_URL=sqlite:///./jovempano.db
```

**Iniciar:**
```bash
uvicorn app.main:app --reload
```

API + docs em `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Portal em `http://localhost:5173`

> O banco de dados e o usuário admin são criados automaticamente na primeira inicialização.

---

## 🧭 Categorias

| Rota | Categoria | Cor |
| :--- | :--- | :--- |
| `/` | Início | Azul |
| `/politica` | Política | Vermelho |
| `/economia` | Economia | Âmbar |
| `/esportes` | Esportes | Esmeralda |
| `/tecnologia` | Tecnologia | Violeta |
| `/entretenimento` | Entretenimento | Rosa |
| `/mundo` | Mundo | Céu |

---

## 🔑 Painel Admin

Acesse `/admin` no navegador. As credenciais são definidas via `.env`. **Nunca use senhas padrão em produção.**

---

## 📁 Estrutura

```
JOVEMPANO/
├── backend/
│   ├── app/
│   │   ├── core/         # Segurança, configuração
│   │   ├── routers/      # news, banners, auth
│   │   ├── models.py     # SQLAlchemy
│   │   ├── schemas.py    # Pydantic
│   │   └── main.py       # Entry point
│   └── .env.example
└── frontend/
    ├── public/images/    # Logo, capas, banners
    └── src/
        ├── components/   # NewsCard, HeroBanner, JellyfishBg, SidebarWidget
        └── views/        # Home, Admin, Politica, Economia, Esportes, Tecnologia, Entretenimento, Mundo
```

---

## 📄 Licença

MIT

---

*Desenvolvido com foco em velocidade e elegância.*
