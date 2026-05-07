from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    print("PING:", response.status_code, response.json())

def test_feeds():
    response = client.get("/feeds/geral?limit=2")
    print("FEEDS GERAL:", response.status_code)
    try:
        data = response.json()
        print("Total Items:", len(data))
        if len(data) > 0:
            print("First item title:", data[0].get("title"))
            print("First item source:", data[0].get("source"))
    except Exception as e:
        print("Error parsing json:", e)

if __name__ == "__main__":
    test_ping()
    test_feeds()
