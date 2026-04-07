import requests
import time
import os
from datetime import datetime

# URL do endpoint de ping (ex: https://seu-app.onrender.com/ping)
# Pega do ENV ou usa o padrão local
API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
PING_ENDPOINT = f"{API_URL.rstrip('/')}/ping"
INTERVAL_MINUTES = 10

def keep_alive():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Keep-Alive iniciado.")
    print(f"Pinging: {PING_ENDPOINT} a cada {INTERVAL_MINUTES} minutos.")
    
    while True:
        try:
            response = requests.get(PING_ENDPOINT, timeout=10)
            if response.status_code == 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Sucesso: {response.json()}")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Falha (Status {response.status_code}): {response.text}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao conectar: {e}")
        
        # Espera o intervalo antes do próximo ping
        time.sleep(INTERVAL_MINUTES * 60)

if __name__ == "__main__":
    keep_alive()
