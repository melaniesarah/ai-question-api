# AI Question API

> A simple FastAPI application that receives questions, validates requests, and processes them through an AI API.

**Repository**: `ai-question-api`

## Features

- Simple and clean project structure
- AI question processing endpoints
- Request validation using Pydantic models
- Automatic API documentation with Swagger UI
- Health check endpoint
- In-memory storage for demo purposes
- Comprehensive testing setup

## Project Structure

```
fastapi/
├── app/
│   ├── __init__.py      # Package initialization
│   ├── main.py          # Main FastAPI application
│   ├── router.py        # API router configuration
│   └── endpoints.py     # Endpoint functions
├── tests/
│   ├── __init__.py      # Test package initialization
│   └── test_endpoints.py # Test cases
├── venv/                 # Virtual environment
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Setup

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - Interactive API docs: http://localhost:8000/docs
   - Alternative API docs: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Welcome message
- `GET /health` - Check if the service is running

### AI Questions
- `POST /api/v1/ask` - Send a question to AI and get response
- `GET /api/v1/questions` - Get all processed questions

## Example Usage

### Ask an AI question
```bash
curl -X POST "http://localhost:8000/api/v1/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is FastAPI?",
       "context": "Python web framework"
     }'
```

### Get all processed questions
```bash
curl -X GET "http://localhost:8000/api/v1/questions"
```

## Request/Response Models

### Question Request
```json
{
  "question": "string (required, 1-1000 chars)",
  "context": "string (optional, max 2000 chars)"
}
```

### Question Response
```json
{
  "question": "string",
  "answer": "string",
  "model": "string (default: gpt-3.5-turbo)"
}
```

## Testing

Run the test suite:
```bash
source venv/bin/activate
pytest tests/
```

## Development

- **Simple Structure**: Only 4 main files for easy maintenance
- **Clean Separation**: Main app, router, and endpoints are separate
- **Validation**: Pydantic models for request/response validation
- **Error Handling**: Basic HTTP error handling
- **Testing**: Simple test setup with pytest
- **API Documentation**: Automatic OpenAPI docs generation

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `httpx` - HTTP client for testing
- `pytest` - Testing framework

## Next Steps

To extend this simple project, consider adding:
- Real AI API integration (OpenAI, Anthropic, etc.)
- Database integration for persistent storage
- Authentication and rate limiting
- Environment configuration
- Docker containerization
- CI/CD pipeline 