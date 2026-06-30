from fastapi.testclient import TestClient

from app.schemas import SourceSnippet
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "qwen_configured" in response.json()


def test_qwen_health_endpoint():
    response = client.get("/api/qwen-health")
    assert response.status_code == 200
    assert "configured" in response.json()


def test_chat_returns_answer_and_type():
    response = client.post(
        "/api/chat",
        json={"question": "广东物理类多少分能报深北莫", "profile": {"province": "广东", "category": "物理类"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] in {"score_query", "comparison_or_advice"}
    assert "不能" in data["answer"] or "分数线" in data["answer"]


def test_program_endpoint_and_chat():
    response = client.get("/api/programs", params={"level": "本科", "degree_mode": "单学籍"})
    assert response.status_code == 200
    assert response.json()["count"] > 0

    chat = client.post(
        "/api/chat",
        json={"question": "电子与计算机工程是单学籍还是双学籍？", "profile": {}},
    )
    assert chat.status_code == 200
    data = chat.json()
    assert data["question_type"] == "program_info"
    assert data["program_rows"]
    assert any(row["program"] == "电子与计算机工程" for row in data["program_rows"])
    assert all(row["program"] == "电子与计算机工程" for row in data["program_rows"])


def test_graduate_program_chat():
    response = client.post(
        "/api/chat",
        json={"question": "纳米生物技术硕士是英语教学吗，招多少人？", "profile": {}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] == "graduate_admission"
    assert data["program_rows"]


def test_greeting_does_not_dump_sources():
    response = client.post("/api/chat", json={"question": "你好", "profile": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] == "greeting"
    assert data["sources"] == []
    assert "可以帮你查" in data["answer"]


def test_clarification_does_not_dump_sources():
    response = client.post("/api/chat", json={"question": "啥意思", "profile": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] == "clarification"
    assert data["sources"] == []
    assert "补充一个方向" in data["answer"]


def test_daily_chat_keeps_assistant_identity():
    response = client.post("/api/chat", json={"question": "你是谁", "profile": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] == "daily_chat"
    assert data["sources"] == []
    assert "深北莫" in data["answer"]


def test_daily_chat_joke_is_bounded():
    response = client.post("/api/chat", json={"question": "讲个笑话", "profile": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] == "daily_chat"
    assert len(data["answer"]) < 120
    assert data["answer"].count("报考助手") <= 1


def test_undergraduate_enrollment_boundary():
    response = client.post("/api/chat", json={"question": "本科招生人数是多少？", "profile": {}})
    assert response.status_code == 200
    data = response.json()
    assert data["question_type"] == "program_info"
    assert data["dimension_rows"]
    assert "招生人数" in data["answer"]


def test_web_search_endpoint(monkeypatch):
    def fake_search_web(query, *, limit=3, timeout=10):
        return [
            SourceSnippet(
                source_id="web_search",
                title="联网搜索：深圳北理莫斯科大学招生通知",
                url="https://admission.smbu.edu.cn/info/example.htm",
                snippet="官方招生通知摘要",
            )
        ]

    monkeypatch.setattr("app.main.web_search.search_web", fake_search_web)
    response = client.get("/api/web-search", params={"q": "最新招生通知"})
    assert response.status_code == 200
    data = response.json()
    assert data["results"][0]["source_id"] == "web_search"


def test_chat_can_enable_web_search(monkeypatch):
    def fake_search_web(query, *, limit=3, timeout=10):
        return [
            SourceSnippet(
                source_id="web_search",
                title="联网搜索：深圳北理莫斯科大学最新招生通知",
                url="https://admission.smbu.edu.cn/info/latest.htm",
                snippet="最新官方网页摘要",
            )
        ]

    monkeypatch.setattr("app.main.web_search.search_web", fake_search_web)
    response = client.post(
        "/api/chat",
        json={"question": "联网搜索深北莫最新招生通知", "profile": {}, "enable_web_search": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert any(source["source_id"] == "web_search" for source in data["sources"])
    assert any("联网搜索" in warning for warning in data["warnings"])
