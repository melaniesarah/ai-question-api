import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.controllers.questions import ask_question, QuestionRequest

client = TestClient(app)


def test_ask_question():
    question_data = {"question": "What is FastAPI?", "context": "Python web framework"}
    response = client.post("/api/v1/ask", json=question_data)
    assert response.status_code == 200
    assert "question" in response.json()
    assert "answer" in response.json()


def test_ask_empty_question():
    question_data = {"question": "", "context": "Empty question"}
    response = client.post("/api/v1/ask", json=question_data)
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


def test_get_questions():
    response = client.get("/api/v1/questions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_ask_question_calls_openai_generate_response():
    with patch("app.controllers.questions.OpenAIClient") as mock_openai_client_class:
        mock_openai_client = MagicMock()
        mock_openai_client.generate_response.return_value = "AI generated response"
        mock_openai_client_class.return_value = mock_openai_client

        test_question = "What is machine learning?"
        request = QuestionRequest(question=test_question)

        result = await ask_question(request)

        mock_openai_client.generate_response.assert_called_once_with(test_question)

        assert result.answer == "AI generated response"
