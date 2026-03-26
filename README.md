<div align="center">
  <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D" alt="Vue.js" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />

  <h1 align="center">📰 JOVEMPANO (Versão Essencial)</h1>
  <p align="center">
    O portal editorial mais seguro, rápido e prático de se administrar. 
    Uma plataforma focada em estabilidade extrema e manutenção livre de estresse via <i>Keep It Simple, Stupid (KISS)</i>.
  </p>
</div>

---

## 🚀 Filosofia do Projeto
Após sucessivos testes empíricos de escalabilidade, o **JOVEMPANO** passou pelo **Pivot Arquitetural Máximo**.
Descartamos orquestrações complexas de Inteligência Artificial, filas assíncronas (Celery/RabbitMQ) e bancos robustos em nuvem para focar 100% em **produtividade real e barata**. O resultado é uma infraestrutura de dois corações: uma API super leve e uma vitrine absurdamente veloz.

## 🏗️ Arquitetura Atômica

| Serviço | Stack Tecnológica | O que faz? |
| :--- | :--- | :--- |
| **O Motor (Backend)** | **Python / FastAPI** | Recebe e entrega os dados em milissegundos. Endpoints enxutos, sem gordura de frameworks velhos. O banco de dados é puramente **SQLite** (um único arquivo físico, imortal). |
| **A Vitrine (Frontend)** | **Vite / Vue 3 / Tailwind** | A face que os leitores veem (`/`). Renderização moderna de uma SPA (Single Page Application) fluída, elegante, rica em interações usando as paletas nativas Tailwind (Dark Slate & Rose). |
| **O Cofre (Moderação)**| **JWT / Moderação** | A rota escondida `/admin` fechada a 7 chaves por criptografia JWT bcrypt. Ela previne desastres permitindo apenas publicações de redatores certificados. |

---

## ⚙️ Instalação Expresso (Zero Docker)

A maior vantagem desta arquitetura é a execução em ambiente host local total **sem necessidade de Docker**. Ligar ou desligar este projeto custa zero esforço sistêmico.

### 1. Injetando a Vida no Backend
```bash
git clone https://github.com/RafaHop3/JOVEMPANO.git
cd JOVEMPANO/backend

# Crie e ative sua bolha ambiente
python -m venv venv
# Linux/Mac: source venv/bin/activate
# Windows: venv\Scripts\activate

pip install -r requirements.txt

# Aperte os cintos e de a ignição
uvicorn app.main:app --reload
```
A API desperta na porta `:8000`. 
✨ **Atenção Magica:** As tabelas SQLite são criadas sozinhas na primeira fração de segundo que o servidor online.
🔐 O superusuário administrador é injetado com as credenciais padrão: `admin` / `admin`.

### 2. Rodando a Vitrine Frontend
Deixe o terminal do Backend aberto, inicie o segundo terminal para o Cliente:
```bash
cd frontend
npm install
npm run dev
```
O console exibirá o caminho estelar da Vitrine em sua máquina (geralmente `http://localhost:5173`). Seu portal está vivo! Basta arrastar o ponteiro p/ página de administração e iniciar as primeiras fofocas públicas.

---

## 🛡️ Contribuições e Cyber-Segurança
A branch `main` é sagrada. Desenvolva novas features através de branches seminais como `feature/design-update`.
⚠️ **Regra de Ouro Pro Deploy:** *Nunca efetue o hospedo desta aplicação mantendo a porta aberta pro Superusuário Legado. A plataforma foi programada para capturar variáveis `.env`, então não hesite em cravar: `ADMIN_PASSWORD="MyUltraSecretPass"` no painel do Host de Deploy!*
