"""
Script para inserir a notícia da comparação Irã x Monarquias do Golfo no banco.
Execute APÓS o backend estar rodando:
  python insert_news.py
  ou
  python insert_news.py https://seu-backend.onrender.com
"""
import sys
import requests

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

# 1. Login
print("🔐 Fazendo login no backend...")
resp = requests.post(
    f"{BASE_URL}/auth/login",
    data={"username": "admin", "password": "admin123"},
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)
resp.raise_for_status()
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
print("✅ Login OK!")

# 2. Inserir notícia
NEWS_ITEM = {
    "title": "Comparação – Irã x Monarquias do Golfo (com questão LGBT)",
    "content": (
        "Uma análise comparativa entre o Irã e as principais monarquias do Golfo Pérsico revela "
        "diferenças e semelhanças surpreendentes em seis dimensões políticas e sociais.\n\n"
        "**Eleições:** O Irã possui eleição presidencial direta (embora o poder real esteja com o "
        "Líder Supremo), enquanto todos os países do Golfo — Arábia Saudita, Bahrein, Kuwait, Omã, "
        "Qatar e EAU — são governados por monarcas ou emires que chegam ao poder por sucessão.\n\n"
        "**Parlamento com mulheres:** Irã, Bahrein, Kuwait e EAU possuem parlamentos com representação "
        "feminina. A Arábia Saudita tem apenas conselho consultivo nomeado. Qatar tem participação mínima. "
        "Os EAU se destacam com 50% dos assentos reservados para mulheres.\n\n"
        "**Mulheres na TV/Mídia:** Todos os países permitem a presença de mulheres na televisão, "
        "ainda que com restrições variadas de cunho religioso ou cultural.\n\n"
        "**Mulheres no volante:** O Irã sempre permitiu mulheres dirigindo. A Arábia Saudita só autorizou "
        "em 2018. Todos os outros países do Golfo já permitiam há décadas.\n\n"
        "**Judeus no parlamento:** Apenas o Irã possui representação judaica garantida por lei (1 assento). "
        "Nenhum dos países do Golfo tem representação judaica.\n\n"
        "**Homossexualidade:** Criminalizada em todos os países analisados. As punições variam: "
        "na Arábia Saudita e no Irã podem incluir pena de morte. Nos EAU, há maior tolerância social "
        "em áreas cosmopolitas como Dubai e Abu Dhabi, embora a lei ainda preveja punições severas."
    ),
    "image_url": None
}

print("📰 Inserindo notícia...")
resp = requests.post(f"{BASE_URL}/news/", json=NEWS_ITEM, headers=headers)
resp.raise_for_status()
data = resp.json()
print(f"✅ Notícia inserida com ID: {data['id']}")
print(f"   Título: {data['title']}")
print(f"   Criada em: {data['created_at']}")
