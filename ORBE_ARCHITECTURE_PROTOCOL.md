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

## 4. Design System e UI/UX (Aesthetics)

O padrao de UI adotado pela OrbeSystems baseia-se em Dark Mode e estetica Cyberpunk/Command Center (especialmente para paineis administrativos), com elementos premium e modernos.

### 4.1 Paleta de Cores e Temas

- Predominancia de fundos escuros (`#09090b` e tons profundos de grafite/preto).
- Cores neon/vibrantes como acentos (no JovemPano: brand rosa/roxo via `var(--brand)`).
- Categorias e tags com cores proprias e bem demarcadas.

### 4.2 Efeitos Visuais Premium

- **Glassmorphism**: headers e paineis fixos com fundos translucidos (`rgba(...)`) e `backdrop-filter: blur(16px)`.
- **Micro-animacoes**: hover states precisos (`transform`, `transition-all`, `duration-300`).
- **Indicadores dinamicos**: status "Ao Vivo" com efeito pulse.

### 4.3 Tipografia

- Combinacao de fontes sem serifa modernas (ex.: Inter ou nativas do sistema) com monospace (ex.: JetBrains Mono) para indicadores tecnicos, datas e labels.

## 5. Deployment e Infraestrutura

Padroes de publicacao previstos:

- **Frontend**: plataformas serverless/CDN como Vercel ou Netlify; `vite build` gera `dist` para servico estatico.
- **Backend**: Render, AWS ou DigitalOcean; execucao via Uvicorn com porta da plataforma (`$PORT`).

---

Este protocolo deve ser consultado e seguido para garantir padronizacao, estetica premium e resiliencia tecnica que definem a qualidade dos sistemas OrbeSystems Technologies.
