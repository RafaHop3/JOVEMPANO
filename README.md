<div align="center">
  <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" alt="Vue.js" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />

  <h1 align="center">📰 JOVEMPANO (Versão Essencial Premium)</h1>
  <p align="center">
    O portal editorial mais elegante, ágil e blindado do mercado. 
    Esculpido com o Padrão de Design <b>StormGamer</b> e enraizado na cartilha <i>Keep It Simple, Stupid (KISS)</i>.
  </p>
</div>

---

## 🚀 Filosofia Mestra
O **JOVEMPANO** passou pela purificação cirúrgica máxima. Removemos a gordura de tecnologias em nuvem, automações complexas (Workers/Celery) e dependências severas. O projeto respira leve: uma **API Síncrona Imbatível** de manutenção barata acoplada a um **Frontend SPA Absurdamente Veloz**, com sistema SEO dinâmico (`@unhead/vue`) pronto para estourar no Google e WhatsApp.

## 🏗️ Arquitetura Atômica

| Camada | Stack Base | Impacto Visual/Funcional |
| :--- | :--- | :--- |
| **O Banco & Motor (Backend)** | **FastAPI / SQLite** | Rotas limpas para ler e postar matérias. Tão enxuto que o Banco de Dados inteiro reside em `jovempano.db`. Zero dependência de Docker. Plugar e brincar na hora! |
| **A Vitrine Premium (Frontend)** | **Vue 3 / TailwindCSS** | O Feed desenhado no **Layout Grid 70/30 (Padrão StormGamer)**. Sidebar fixada, alternador mágico de Dark/Light mode e meta-tags OpenGraph de alto rankeamento embutidas na alma das views. |
| **O Cofre Central (Admin)**| **Vue / JWT bcrypt** | Acesso secreto (`/admin`) banido dos menus públicos (Segurança por Ofuscação). Fechado por hash salteado barrando qualquer hacker e concedendo aos revisores a caneta pra publicar na hora. |

---

## ⚙️ Instalação Mágica (Plugar & Usar)

Inicie as turbinas dessa máquina na sua hospedagem ou computador sem depender de nuvens externas:

### 1. Injetando Vida no Backend
```bash
git clone https://github.com/RafaHop3/JOVEMPANO.git
cd JOVEMPANO/backend

# Isolando o ambiente de Python com segurança
python -m venv venv
venv\Scripts\activate # (No Linux/Mac use: source venv/bin/activate)

pip install -r requirements.txt

# Girando a chave
uvicorn app.main:app --reload
```
A API acorda na porta `:8000`. O super-admin será moldado no banco de dados com a permissão:
🔐 **Credenciais do Escritório**: `admin` / `admin` (*Pode e DEVE ser alterado via `.env` em deploy*).

### 2. Ativando a SPA Premium (Vitrine Frontend)
Abra outra ponta de console e corra:
```bash
cd frontend
npm install
npm run dev
```
Navegue logo para `http://localhost:5173`. Prove a fluidez instantânea clicando no ícone do solêmio/lua pra trocar os climas de DarkMode.

---

## 🛡️ Cyber-Segurança Final
Para hospedagem verdadeira debaixo de Domínios públicos (Vercel/Render):
> Não suba o portal cru! Force a injeção da sua senha complexa criando a variável ambiente `ADMIN_PASSWORD="MinhaSenhaCabulosa54"` no servidor provedor e o JOVEMPANO blindará sua chave primária com `bcrypt` no minuto do Start. O CORS já está travado contra cross-scripting hostil!
