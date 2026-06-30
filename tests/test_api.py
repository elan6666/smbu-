from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_returns_answer_and_type():
    response = client.post(
        "/api/chat",
        json={"question": "广东物理类多少分能报深北莫", "profile": {"province": "广东", "category": "物理类"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] in {"score_query", "comparison_or_advice"}
    assert "不能" in data["answer"] or "分数线" in data["answer"]

