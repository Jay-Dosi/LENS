"""
Configuration management for ESG Claim Verification Assistant
Stateless architecture with ChromaDB - NO external storage required
"""
import os
from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # IBM watsonx.ai Configuration (REQUIRED)
    ibm_cloud_api_key: str
    ibm_watsonx_project_id: str
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    # Using ibm/granite-3-8b-instruct for both extraction and explanation
    # This is the closest available IBM Granite instruction-tuned model
    # (granite-13b-instruct-v2 is not available in this environment)
    watsonx_extraction_model: str = "ibm/granite-3-8b-instruct"
    watsonx_explanation_model: str = "ibm/granite-3-8b-instruct"
    
    # IBM Watson NLU Configuration (REQUIRED)
    watson_nlu_api_key: str
    watson_nlu_url: str = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com"
    
    # Storage Configuration - ChromaDB (Stateless)
    storage_mode: Literal["memory", "persistent"] = "memory"  # memory = stateless, persistent = local disk
    storage_persist_directory: str = "./chroma_storage"  # Only used if storage_mode = "persistent"
    session_timeout_minutes: int = 60  # Session timeout in minutes
    
    # NLU Configuration - Watson NLU is configured above
    
    # External APIs
    # OpenWeatherMap Air Pollution API (Optional - free tier: 1000 calls/day)
    openweathermap_api_key: Optional[str] = None
    
    # Application Settings
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 50
    allowed_extensions: str = "pdf"
    log_level: str = "INFO"
    
    # CORS Settings
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # Computed properties
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size to bytes"""
        return self.max_file_size_mb * 1024 * 1024
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Get list of allowed file extensions"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Get list of CORS origins"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    def validate_storage_config(self) -> None:
        """Validate storage configuration"""
        if self.storage_mode == "persistent":
            if not os.path.exists(os.path.dirname(self.storage_persist_directory) or "."):
                os.makedirs(self.storage_persist_directory, exist_ok=True)
    
    def validate_watsonx_config(self) -> None:
        """Validate watsonx.ai configuration"""
        if not self.ibm_cloud_api_key:
            raise ValueError("IBM_CLOUD_API_KEY is required for watsonx.ai")
        if not self.ibm_watsonx_project_id:
            raise ValueError("IBM_WATSONX_PROJECT_ID is required for watsonx.ai")
    
    def validate_watson_nlu_config(self) -> None:
        """Validate Watson NLU configuration"""
        if not self.watson_nlu_api_key:
            raise ValueError("WATSON_NLU_API_KEY is required for Watson NLU")


# Global settings instance
settings = Settings()

# Validate configuration on startup
try:
    settings.validate_watsonx_config()
    settings.validate_watson_nlu_config()
    settings.validate_storage_config()
except ValueError as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Configuration validation warning: {e}")


def get_settings() -> Settings:
    """Dependency injection for FastAPI"""
    return settings

# Made with Bob
