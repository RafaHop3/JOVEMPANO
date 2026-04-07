import os
import sys

# Garante que o diretório atual está no path para importar o módulo 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app import models
from app.core.security import get_password_hash
from app.core.config import settings

def seed_db():
    print("Iniciando o seeding automático do banco de dados JovemPano...")
    
    # Cria as tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Admin User
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            print("Criando usuário admin default...")
            hashed_pw = get_password_hash(settings.ADMIN_PASSWORD or "admin123")
            db.add(models.User(username="admin", hashed_password=hashed_pw, role="admin"))
            db.commit()
        else:
            print("Usuário admin já existe.")

        # 2. Hero Banner
        banner_count = db.query(models.HeroBanner).count()
        if banner_count == 0:
            print("Populando Hero Banner de exemplo...")
            db.add(models.HeroBanner(
                title="JovemPano — O Pulso das Notícias",
                subtitle="Informação sem filtro, com a velocidade que o Brasil exige.",
                image_url="https://images.unsplash.com/photo-1585829365234-781fdfc4190b?q=80&w=2070&auto=format&fit=crop",
                is_active=True
            ))
            db.commit()
        else:
            print(f"{banner_count} banners já encontrados no banco.")

        # 3. News Articles
        news_count = db.query(models.News).count()
        if news_count == 0:
            print("Populando notícias de exemplo...")
            news_items = [
                {
                    "title": "Congresso aprova nova lei de transparência fiscal",
                    "category": "Política",
                    "content": (
                        "O Congresso Nacional aprovou nesta quarta-feira, por ampla maioria, a nova lei de transparência fiscal "
                        "que obriga todos os entes federativos a publicar em tempo real os dados de gastos públicos em portal "
                        "unificado na internet.\n\n"
                        "A medida, considerada histórica por especialistas, deve aumentar o controle social sobre os recursos "
                        "públicos e dificultar desvios de verbas. A lei entra em vigor em 90 dias após a sanção presidencial."
                    ),
                    "image_url": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?q=80&w=2070&auto=format&fit=crop"
                },
                {
                    "title": "Bolsa de valores atinge recorde histórico impulsionada por commodities",
                    "category": "Economia",
                    "content": (
                        "O Ibovespa encerrou o pregão desta terça-feira em alta de 3,2%, atingindo novo recorde histórico ao "
                        "superar os 145 mil pontos, impulsionado pela valorização das ações do setor de mineração e petróleo.\n\n"
                        "A alta das commodities no mercado internacional, especialmente o minério de ferro e o petróleo bruto, "
                        "beneficiou diretamente as grandes exportadoras brasileiras listadas na B3."
                    ),
                    "image_url": "https://images.unsplash.com/photo-1611974714024-4627d3b379d1?q=80&w=2070&auto=format&fit=crop"
                },
                {
                    "title": "Seleção Brasileira vence por 3 a 0 e se classifica para a Copa do Mundo",
                    "category": "Esportes",
                    "content": (
                        "A Seleção Brasileira de futebol garantiu vaga na próxima Copa do Mundo com uma vibrante vitória por "
                        "3 a 0 sobre a Argentina no Maracanã, em partida que lotou o estádio com mais de 78 mil torcedores.\n\n"
                        "Os gols foram marcados por Vini Jr., Rodrygo e um golaço de falta de Neymar no segundo tempo."
                    ),
                    "image_url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2036&auto=format&fit=crop"
                }
            ]
            for n in news_items:
                db.add(models.News(**n))
            db.commit()
            print("Notícias populadas com sucesso.")
        else:
            print(f"{news_count} notícias já encontradas no banco.")

        print("Processo de seeding concluído.")
    except Exception as e:
        print(f"Erro durante o seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
