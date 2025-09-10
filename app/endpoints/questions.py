from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional


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
    """
    Process a question and return AI response.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Simulate AI processing (replace with actual AI API call)
    ai_response = f"AI response to: {request.question}"

    # Store the question and response
    question_data = {
        "question": request.question,
        "answer": ai_response,
        "context": request.context,
    }
    questions_db.append(question_data)

    return QuestionResponse(question=request.question, answer=ai_response)


async def get_questions():
    """
    Get all processed questions.
    """
    return questions_db
