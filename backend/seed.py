"""
Seed script: creates initial news articles with images and a hero banner.
Run once after starting the backend:  python seed.py
"""
import sqlite3, hashlib, os, sys

# The DB will be at backend/jovempano.db
# We'll use the FastAPI startup logic to create tables, 
# then inject through the API once backend is up.
# This script just prints example curl commands.

NEWS = [
    {
        "title": "Congresso aprova nova lei de transparência fiscal",
        "content": (
            "O Congresso Nacional aprovou nesta quarta-feira, por ampla maioria, a nova lei de transparência fiscal "
            "que obriga todos os entes federativos a publicar em tempo real os dados de gastos públicos em portal "
            "unificado na internet.\n\n"
            "A medida, considerada histórica por especialistas, deve aumentar o controle social sobre os recursos "
            "públicos e dificultar desvios de verbas. A lei entra em vigor em 90 dias após a sanção presidencial.\n\n"
            "Para o relator da matéria, deputado João Silva (MDB-SP), a aprovação representa 'um divisor de águas "
            "na relação entre o Estado e o cidadão'. O texto segue agora para o Senado Federal."
        ),
        "image_url": "/images/news_politica.png"
    },
    {
        "title": "Bolsa de valores atinge recorde histórico impulsionada por commodities",
        "content": (
            "O Ibovespa encerrou o pregão desta terça-feira em alta de 3,2%, atingindo novo recorde histórico ao "
            "superar os 145 mil pontos, impulsionado pela valorização das ações do setor de mineração e petróleo.\n\n"
            "A alta das commodities no mercado internacional, especialmente o minério de ferro e o petróleo bruto, "
            "beneficiou diretamente as grandes exportadoras brasileiras listadas na B3.\n\n"
            "Analistas apontam que o cenário externo favorável, combinado com dados positivos da economia doméstica, "
            "cria um ambiente propício para novos recordes nas próximas sessões. O dólar fechou em queda de 0,8%."
        ),
        "image_url": "/images/news_economia.png"
    },
    {
        "title": "Seleção Brasileira vence por 3 a 0 e se classifica para a Copa do Mundo",
        "content": (
            "A Seleção Brasileira de futebol garantiu vaga na próxima Copa do Mundo com uma vibrante vitória por "
            "3 a 0 sobre a Argentina no Maracanã, em partida que lotou o estádio com mais de 78 mil torcedores.\n\n"
            "Os gols foram marcados por Vini Jr., Rodrygo e um golaço de falta de Neymar no segundo tempo. "
            "A atuação da equipe foi elogiada unanimemente pela imprensa especializada.\n\n"
            "Com a classificação antecipada, o técnico Dorival Júnior poderá rodar o elenco nas últimas rodadas "
            "das eliminatórias e testar alternativas táticas antes do torneio mundial."
        ),
        "image_url": "/images/news_esportes.png"
    }
]

BANNER = {
    "title": "JovemPano — O Pulso das Notícias",
    "subtitle": "Informação sem filtro, com a velocidade que o Brasil exige.",
    "image_url": "/images/hero_banner.png",
    "is_active": True
}

TOKEN_PLACEHOLDER = "SEU_TOKEN_AQUI"

print("=" * 60)
print("SEED - Comandos para popular o banco de dados")
print("=" * 60)
print("\n1. Primeiro faça login e copie o token:")
print('curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=admin123"')
print("\n2. Banner destaque:")
import json
print(f'curl -X POST http://127.0.0.1:8000/banners/ -H "Authorization: Bearer {TOKEN_PLACEHOLDER}" -H "Content-Type: application/json" -d \'{json.dumps(BANNER)}\'')
print("\n3. Notícias de exemplo:")
for n in NEWS:
    print(f'curl -X POST http://127.0.0.1:8000/news/ -H "Authorization: Bearer {TOKEN_PLACEHOLDER}" -H "Content-Type: application/json" -d \'{json.dumps(n)}\'')
