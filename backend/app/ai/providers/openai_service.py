from langchain_openai import ChatOpenAI
from app.core.config import settings
from app.core.exceptions import AIProviderException
from app.core.logging import logger

class OpenAIService:
    @staticmethod
    def get_model(temperature: float = 0.2) -> ChatOpenAI:
        """
        Instantiate and return a configured LangChain ChatOpenAI client.
        Uses environment settings for model name and API key.
        """
        api_key = settings.API_KEY or settings.OPENAI_API_KEY
        model_name = settings.MODEL if settings.API_KEY else settings.OPENAI_MODEL
        base_url = settings.BASE_URL if settings.API_KEY else None
        
        if not api_key:
            logger.warning(
                "Neither API_KEY nor OPENAI_API_KEY is set. LangChain OpenAI requests will fail. "
                "Ensure keys are configured in your .env environment variables."
            )
            # We return a dummy mock model to allow tests to run, but actual requests will fail
            return ChatOpenAI(
                model=model_name,
                api_key="dummy_key_for_initialization",
                temperature=temperature,
                max_retries=1,
                timeout=5
            )
            
        try:
            return ChatOpenAI(
                model=model_name,
                api_key=api_key,
                base_url=base_url,
                temperature=temperature,
                max_retries=3,
                timeout=30
            )
        except Exception as e:
            logger.error(f"Failed to initialize ChatOpenAI: {e}", exc_info=True)
            raise AIProviderException("openai", str(e))
