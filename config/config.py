import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    
    AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    DATABASE_URL = os.getenv("DATABASE_URL", "smartlead.db")

    CORS_ALLOWED_ORIGINS = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "*"
    )

    BUSINESS_CONTEXT = os.getenv(
    "BUSINESS_CONTEXT",
    "You are Export AI, an AI-powered international trade and export assistant."
)