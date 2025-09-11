import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is required but not set")


class OpenAIClient:
    def __init__(self):
        self.api_key = OPENAI_API_KEY

    def generate_response(self, prompt: str):
        return "This is a test response"
