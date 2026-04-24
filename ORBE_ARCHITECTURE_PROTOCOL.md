# Protocolo Arquitetural OrbeSystems (Modelo JOVEMPANO)

Este documento descreve a estrutura oficial, tecnologias e convenções derivadas do projeto JOVEMPANO, estabelecendo o modelo padrao para futuros desenvolvimentos full-stack na OrbeSystems Technologies.

## 1. Visao Geral da Arquitetura

A arquitetura adota o padrao de separacao total entre Frontend (SPA) e Backend (API REST), comunicando-se via JSON.

- Frontend: Vue.js 3 + Vite + Tailwind CSS + Vue Router
- Backend: FastAPI (Python) + SQLAlchemy + Pydantic
- Banco de Dados: Relacional (SQLite por padrao local/MVP, com suporte via SQLAlchemy para PostgreSQL/MySQL em producao)

## 2. Estrutura do Backend (FastAPI)

### 2.1 Tecnologias e Dependencias

- `fastapi`, `uvicorn[standard]`
- `sqlalchemy` (ORM)
- `pydantic`, `pydantic-settings` (validacao de dados e configuracoes)
- `passlib[bcrypt]`, `python-jose[cryptography]`, `python-multipart` (autenticacao e seguranca)
- `feedparser`, `beautifulsoup4`, `requests` (ingestao de dados/RSS)

### 2.2 Organizacao de Diretorios

```text
backend/
├── app/
│   ├── core/              # Configuracoes globais e de seguranca (settings, JWT)
│   ├── routers/           # Controladores de rotas (auth, news, feeds, banners)
│   ├── database.py        # Configuracao da engine SQLAlchemy e sessao
│   ├── main.py            # Ponto de entrada FastAPI, middlewares (CORS), e lifespan
│   ├── models.py          # Modelos de banco de dados (SQLAlchemy)
│   └── schemas.py         # Schemas de validacao de dados (Pydantic)
├── requirements.txt
└── jovempano.db           # Banco de dados local (SQLite)
```

### 2.3 Convencoes Backend

- **Lifespan Context**: utilizar o lifespan do FastAPI no `main.py` para criacao de tabelas (`Base.metadata.create_all`) e seed do banco de dados (ex.: criacao de usuario admin padrao).
- **Injecao de Dependencia**: a sessao do banco deve ser injetada nas rotas via `Depends(get_db)`.
- **Autenticacao**: fluxo padrao baseado em JWT (JSON Web Tokens); senhas devem ser hasheadas com `bcrypt`.
- **Modelos principais**:
  - `User`: gerenciamento de credenciais (admin).
  - `News`: armazenamento de postagens e artigos.
  - `HeroBanner`: gerenciamento dos destaques visuais de topo.

### 2.4 Seguranca (obrigatorio em producao)

- **Sem credenciais no codigo**: `ADMIN_USERNAME`, `ADMIN_PASSWORD` e `SECRET_KEY` vêm de variáveis de ambiente (veja `backend/.env.example`).
- **CORS restrito por origem**: use `FRONTEND_URL` e, se necessário, `EXTRA_CORS_ORIGINS` para cada dominio do frontend.
- **Publicacao apenas autenticada**: rotas `POST/PUT/DELETE` de notícias e banners exigem JWT (`Depends(get_current_user)`).
- **Painel isolado na rota `/admin`**: o site publico nao exibe atalhos de login ou publicacao; acesso administrativo e somente nessa rota, com autenticacao.
- **Headers HTTP**: middleware basico (ex.: `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`).

## 3. Estrutura do Frontend (Vue 3 + Vite)

### 3.1 Tecnologias e Dependencias

- `vue` (`^3.5.x`)
- `vite` (`^5.4.x`)
- `vue-router` (`^4.4.x`)
- `tailwindcss` (v3.4.x ou v4.x com PostCSS)
- `quill` (editor rich text para Admin)

### 3.2 Organizacao de Diretorios

```text
frontend/
├── public/                # Assets estaticos servidos diretamente
├── src/
│   ├── assets/            # Imagens e vetores base
│   ├── components/        # Componentes reutilizaveis (ex.: NewsCard, FeedCard, CookieBanner)
│   ├── views/             # Telas principais roteadas (Home, Admin, NewsDetail, CategoryView)
│   ├── App.vue            # Layout raiz (Header global, navegacao, main content e footer)
│   ├── entry.js/main.js   # Ponto de entrada, configuracao de rotas e mount do app
│   └── style.css          # Estilos globais Vanilla CSS e diretivas Tailwind
├── package.json
├── tailwind.config.js     # Temas, cores, fontes (Design System)
└── vite.config.js
```

### 3.3 Convencoes Frontend

- **Roteamento estavel**: evitar importacoes dinamicas (`() => import(...)`) para rotas principais em cenarios com historico de falhas de carregamento em producao; usar static imports no roteador para estabilidade maxima.
- **SEO por rota**: utilizar `router.afterEach` para atualizar dinamicamente `document.title` com base em `meta.title` das rotas.
- **Composicao visual**: `App.vue` atua como wrapper estrutural, gerindo exibicao condicional de elementos globais (ex.: remover header e footer em `/admin`).
- **API em producao**: definir `VITE_API_URL` (ex.: `frontend/.env.production` ou variaveis no painel do host) apontando para a URL publica do backend.

## 4. Design System e UI/UX (Aesthetics)

O padrão de UI adotado pela OrbeSystems baseia-se na estética Cyberpunk/Terminal, criando uma experiência imersiva de Command Center com elementos premium e focados no aspecto técnico/SecDevOps.

### 4.1 Paleta de Cores e Temas

- **Background**: `terminal-bg` (Preto Profundo / Navy), proporcionando imersão total no dark mode.
- **Acentos Neon**: `neon-cyan` (#00fff5), `neon-green` (#39ff14), `neon-purple` (#bc13fe), `neon-blue` (#0066ff) utilizados para destaques, interações e feedback.
- **Texto**: Branco puro para conteúdo primário; `terminal-muted` (Cinza/Azul-Cinza) para descrições técnicas e metadados.

### 4.2 Efeitos Visuais Premium e Animações

- **Glassmorphism Terminal**: Paineis e headers com fundos translúcidos e `backdrop-filter`.
- **Micro-animações**:
  - `animate-pulse-neon` para indicadores de status (como "Ao Vivo").
  - `animate-spin-slow` e SVG animados para logos e elementos de carregamento.
- **Bordas Técnicas**: Elementos interativos utilizam box-shadows com cores neon sutis para feedback visual.

### 4.3 Tipografia

- Combinacao de fontes sem serifa modernas (ex.: Inter ou nativas do sistema) com monospace (ex.: JetBrains Mono) para indicadores tecnicos, datas e labels.

## 5. Deployment e Infraestrutura

Padroes de publicacao previstos:

- **Frontend**: plataformas serverless/CDN como Vercel ou Netlify; `vite build` gera `dist` para servico estatico.
- **Backend**: Render, AWS ou DigitalOcean; execucao via Uvicorn com porta da plataforma (`$PORT`).

---

Este protocolo deve ser consultado e seguido para garantir padronizacao, estetica premium e resiliencia tecnica que definem a qualidade dos sistemas OrbeSystems Technologies.
