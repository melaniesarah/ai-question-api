from fastapi import APIRouter
from app.endpoints import ask_question, get_questions

router = APIRouter(prefix="/api/v1")

# AI question endpoints
router.add_api_route("/ask", ask_question, methods=["POST"], tags=["AI Questions"])
router.add_api_route("/questions", get_questions, methods=["GET"], tags=["AI Questions"])