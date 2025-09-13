import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.controllers.questions import (
    ask_question,
    QuestionRequest,
    QuestionResponse,
    questions_db,
)

client = TestClient(app)


class TestQuestionsController:
    def setup_method(self):
        questions_db.clear()

    def test_ask_question_success_with_context(self):
        with patch("app.controllers.questions.OpenAIClient") as mock_openai_class:
            mock_openai_client = MagicMock()
            mock_openai_client.generate_response.return_value = (
                "FastAPI is a modern Python web framework for building APIs."
            )
            mock_openai_class.return_value = mock_openai_client

            question_data = {
                "question": "What is FastAPI?",
                "context": "Python web framework",
            }
            response = client.post("/api/v1/ask", json=question_data)

            assert response.status_code == 200
            response_data = response.json()
            assert response_data["question"] == "What is FastAPI?"
            assert (
                response_data["answer"]
                == "FastAPI is a modern Python web framework for building APIs."
            )
            assert response_data["model"] == "gpt-3.5-turbo"

            mock_openai_class.assert_called_once()
            mock_openai_client.generate_response.assert_called_once_with(
                prompt="What is FastAPI?", context="Python web framework"
            )

    def test_ask_question_success_without_context(self):
        with patch("app.controllers.questions.OpenAIClient") as mock_openai_class:
            mock_openai_client = MagicMock()
            mock_openai_client.generate_response.return_value = (
                "Machine learning is a subset of artificial intelligence."
            )
            mock_openai_class.return_value = mock_openai_client

            question_data = {"question": "What is machine learning?"}
            response = client.post("/api/v1/ask", json=question_data)

            assert response.status_code == 200
            response_data = response.json()
            assert response_data["question"] == "What is machine learning?"
            assert (
                response_data["answer"]
                == "Machine learning is a subset of artificial intelligence."
            )

            mock_openai_class.assert_called_once()
            mock_openai_client.generate_response.assert_called_once_with(
                prompt="What is machine learning?", context=None
            )

    def test_ask_empty_question(self):
        question_data = {"question": "", "context": "Empty question"}
        response = client.post("/api/v1/ask", json=question_data)

        assert response.status_code == 400
        assert "Question cannot be empty" in response.json()["detail"]

    def test_ask_whitespace_only_question(self):
        question_data = {"question": "   ", "context": "Whitespace question"}
        response = client.post("/api/v1/ask", json=question_data)

        assert response.status_code == 400
        assert "Question cannot be empty" in response.json()["detail"]

    def test_ask_question_openai_error(self):
        with patch("app.controllers.questions.OpenAIClient") as mock_openai_class:
            mock_openai_client = MagicMock()
            mock_openai_client.generate_response.side_effect = Exception(
                "API rate limit exceeded"
            )
            mock_openai_class.return_value = mock_openai_client

            question_data = {"question": "What is AI?", "context": "Technology"}
            response = client.post("/api/v1/ask", json=question_data)

            assert response.status_code == 500
            assert (
                "Failed to generate AI response: API rate limit exceeded"
                in response.json()["detail"]
            )

            mock_openai_class.assert_called_once()

    def test_ask_question_stores_in_database(self):
        with patch("app.controllers.questions.OpenAIClient") as mock_openai_class:
            mock_openai_client = MagicMock()
            mock_openai_client.generate_response.return_value = "Test answer"
            mock_openai_class.return_value = mock_openai_client

            question_data = {"question": "Test question?", "context": "Test context"}
            response = client.post("/api/v1/ask", json=question_data)

            assert response.status_code == 200
            assert len(questions_db) == 1

            stored_question = questions_db[0]
            assert stored_question["question"] == "Test question?"
            assert stored_question["answer"] == "Test answer"
            assert stored_question["context"] == "Test context"

            mock_openai_class.assert_called_once()

    def test_get_questions_empty(self):
        questions_db.clear()
        response = client.get("/api/v1/questions")

        assert response.status_code == 200
        assert response.json() == []

    def test_get_questions_with_data(self):
        questions_db.clear()
        questions_db.extend(
            [
                {
                    "question": "What is Python?",
                    "answer": "Python is a programming language.",
                    "context": "Programming",
                },
                {
                    "question": "What is FastAPI?",
                    "answer": "FastAPI is a web framework.",
                    "context": "Web development",
                },
            ]
        )

        response = client.get("/api/v1/questions")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["question"] == "What is Python?"
        assert data[1]["question"] == "What is FastAPI?"

    @pytest.mark.asyncio
    async def test_ask_question_function_direct(self):
        with patch("app.controllers.questions.OpenAIClient") as mock_openai_class:
            mock_openai_client = MagicMock()
            mock_openai_client.generate_response.return_value = "Direct test response"
            mock_openai_class.return_value = mock_openai_client

            questions_db.clear()

            test_question = "What is testing?"
            test_context = "Software development"
            request = QuestionRequest(question=test_question, context=test_context)

            result = await ask_question(request)

            mock_openai_class.assert_called_once()
            mock_openai_client.generate_response.assert_called_once_with(
                prompt=test_question, context=test_context
            )

            assert isinstance(result, QuestionResponse)
            assert result.question == test_question
            assert result.answer == "Direct test response"
            assert result.model == "gpt-3.5-turbo"

            assert len(questions_db) == 1
            stored = questions_db[0]
            assert stored["question"] == test_question
            assert stored["answer"] == "Direct test response"
            assert stored["context"] == test_context

    def test_multiple_questions_accumulation(self):
        with patch("app.controllers.questions.OpenAIClient") as mock_openai_class:
            mock_openai_client = MagicMock()
            mock_openai_client.generate_response.return_value = "Test answer"
            mock_openai_class.return_value = mock_openai_client

            questions_db.clear()

            response1 = client.post("/api/v1/ask", json={"question": "Question 1?"})
            assert response1.status_code == 200
            assert len(questions_db) == 1

            response2 = client.post("/api/v1/ask", json={"question": "Question 2?"})
            assert response2.status_code == 200
            assert len(questions_db) == 2

            assert questions_db[0]["question"] == "Question 1?"
            assert questions_db[1]["question"] == "Question 2?"

            assert mock_openai_class.call_count == 2
