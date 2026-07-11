import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "EduPilot AI"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Database Settings
    # Use SQLite + aiosqlite by default for async SQL operations in dev
    DATABASE_URL: str = "sqlite+aiosqlite:///./edupilot.db"

    # AI API Keys & Models
    OPENAI_API_KEY: str = Field(default="", validation_alias="OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o-mini"

    COHERE_API_KEY: str = Field(default="", validation_alias="COHERE_API_KEY")
    COHERE_MODEL: str = "command-r-plus-08-2024"

    # ML Paths
    MODEL_PATH: str = "./artifacts/models/student_risk_ann.pt"
    PREPROCESSOR_PATH: str = "./artifacts/preprocessors/preprocessor.joblib"
    LABEL_ENCODER_PATH: str = "./artifacts/preprocessors/label_encoder.joblib"
    METADATA_PATH: str = "./artifacts/models/model_metadata.json"
    EXPLAINER_PATH: str = "./artifacts/explainers/shap_explainer.joblib"

    # Custom LLM Settings (e.g. Groq)
    API_KEY: str = Field(default="", validation_alias="API_KEY")
    MODEL: str = Field(default="llama-3.1-8b-instant", validation_alias="MODEL")
    BASE_URL: str = Field(default="https://api.groq.com/openai/v1", validation_alias="BASE_URL")

    # File Upload & Reports Storage
    UPLOAD_DIR: str = "./uploads"
    REPORT_DIR: str = "./generated_reports"
    MAX_UPLOAD_SIZE_MB: int = 10

    # CORS Settings
    FRONTEND_URL: str = "http://localhost:5173"

    # Load environment variables from .env file inside backend directory
    model_config = SettingsConfigDict(
        env_file=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
