import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_all

# Adiciona o diretório atual ao path para importar a app
sys.path.append(os.getcwd())

from app.database import SessionLocal, engine, Base
from app import models
from app.core.security import get_password_hash

def seed():
    print("Iniciando semeadura automática do banco de dados...")
    
    # Cria as tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Criar Admin padrão
        admin_pass = os.getenv("ADMIN_PASSWORD", "admin123")
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin:
            print("Criando usuário admin...")
            db.add(models.User(
                username="admin", 
                hashed_password=get_password_hash(admin_pass),
                role="admin"
            ))
        
        # 2. Criar Notícias de Exemplo com Categorias
        if db.query(models.News).count() == 0:
            print("Criando notícias de exemplo...")
            sample_news = [
                {
                    "title": "Economia Brasileira cresce 3% no trimestre",
                    "content": "O PIB brasileiro apresentou um crescimento robusto impulsionado pelo agronegócio e serviços.",
                    "category": "Economia",
                    "image_url": "/images/news_economia.png"
                },
                {
                    "title": "Novas medidas na Política de Saúde",
                    "content": "O governo anunciou um novo pacote de investimentos para hospitais regionais.",
                    "category": "Política",
                    "image_url": "/images/news_politica.png"
                },
                {
                    "title": "Tecnologia 5G avança em todo o país",
                    "content": "Mais de 500 cidades agora contam com cobertura total de rede 5G de alta velocidade.",
                    "category": "Tecnologia",
                    "image_url": "/images/news_tecnologia.png"
                }
            ]
            for n in sample_news:
                db.add(models.News(**n))
        
        # 3. Criar Banners de Destaque
        if db.query(models.HeroBanner).count() == 0:
            print("Criando banners de destaque...")
            db.add(models.HeroBanner(
                title="JOVEMPANO PREMIUM",
                subtitle="A informação que você confia, com a agilidade que você precisa.",
                image_url="/images/hero_banner.png",
                is_active=True
            ))

        db.commit()
        print("Semeadura concluída com sucesso!")
    except Exception as e:
        print(f"Erro ao semear: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
