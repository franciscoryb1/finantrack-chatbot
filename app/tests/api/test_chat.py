from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_chat_clarification_flow():
    # Paso 1: falta período
    r1 = client.post("/chat", json={
        "userId": "u1",
        "text": "cuánto gasté"
    })

    body1 = r1.json()

    assert body1["needsClarification"] is True
    assert "período" in body1["replyText"].lower()

    # Paso 2: follow-up
    r2 = client.post("/chat", json={
        "userId": "u1",
        "text": "este mes"
    })

    body2 = r2.json()

    assert body2["needsClarification"] is False
    assert "gastaste" in body2["replyText"].lower()


def test_chat_balance():
    r = client.post("/chat", json={
        "userId": "u2",
        "text": "saldo"
    })

    body = r.json()

    assert body["needsClarification"] is False
    assert "saldo" in body["replyText"].lower()
