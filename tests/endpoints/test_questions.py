from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_ask_question():
    """Test asking a question returns proper response."""
    question_data = {"question": "What is FastAPI?", "context": "Python web framework"}
    response = client.post("/api/v1/ask", json=question_data)
    assert response.status_code == 200
    assert "question" in response.json()
    assert "answer" in response.json()


def test_ask_empty_question():
    """Test asking empty question returns error."""
    question_data = {"question": "", "context": "Empty question"}
    response = client.post("/api/v1/ask", json=question_data)
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


def test_get_questions():
    """Test getting all questions returns list."""
    response = client.get("/api/v1/questions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
