from fastapi import APIRouter
from app.endpoints.core import root, health
from app.endpoints.questions import ask_question, get_questions

# Main router for API v1 endpoints
router = APIRouter(prefix="/api/v1")

# AI question endpoints
router.add_api_route("/ask", ask_question, methods=["POST"], tags=["AI Questions"])
router.add_api_route(
    "/questions", get_questions, methods=["GET"], tags=["AI Questions"]
)

# Root router for basic endpoints (no prefix)
root_router = APIRouter()

# Root and health endpoints
root_router.add_api_route("/", root, methods=["GET"], tags=["Basic"])
root_router.add_api_route("/health", health, methods=["GET"], tags=["Basic"])
