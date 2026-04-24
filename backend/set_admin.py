import sys
import os

# Adiciona o diretório atual ao path para importar a pasta 'app'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import User
from app.core.security import get_password_hash

def main():
    db = SessionLocal()
    
    username = "rafael_admin"
    password = "Muhammadalivsroyjonesjr"

    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            user.hashed_password = get_password_hash(password)
            print(f"[!] Usuário '{username}' já existia. A senha foi atualizada com sucesso.")
        else:
            new_user = User(username=username, hashed_password=get_password_hash(password), role="admin")
            db.add(new_user)
            print(f"[+] Usuário '{username}' criado com sucesso.")

        db.commit()
    except Exception as e:
        print(f"Erro ao acessar o banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
