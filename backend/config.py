from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import os


BASE_URL=os.getenv("BASE_URL", "https://api.groq.com/openai/v1")
API_KEY=os.getenv("API_KEY")
MODEL=os.getenv("MODEL")    