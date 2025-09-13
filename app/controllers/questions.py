from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from app.openai_client import OpenAIClient


# Request/Response models
class QuestionRequest(BaseModel):
    question: str
    context: Optional[str] = None


class QuestionResponse(BaseModel):
    question: str
    answer: str
    model: str = "gpt-3.5-turbo"


# In-memory storage for demo
questions_db = []


async def ask_question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        openai_client = OpenAIClient()

        ai_response = openai_client.generate_response(
            prompt=request.question, context=request.context
        )

        question_data = {
            "question": request.question,
            "answer": ai_response,
            "context": request.context,
        }
        questions_db.append(question_data)

        return QuestionResponse(question=request.question, answer=ai_response)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate AI response: {str(e)}"
        )


async def get_questions():
    return questions_db
