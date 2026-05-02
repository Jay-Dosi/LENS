"""
Configuration management for ESG Claim Verification Assistant
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # IBM Cloud Configuration
    ibm_cloud_api_key: str
    ibm_watsonx_project_id: str
    
    # IBM Cloud Object Storage
    ibm_cos_endpoint: str
    ibm_cos_api_key: str
    ibm_cos_instance_crn: str
    ibm_cos_bucket_name: str = "esg-lens-hackathon"
    
    # IBM Watson Natural Language Understanding
    ibm_nlu_api_key: str
    ibm_nlu_url: str
    
    # watsonx.ai Configuration
    watsonx_url: str = "https://us-south.ml.cloud.ibm.com"
    watsonx_extraction_model: str = "ibm/granite-13b-instruct-v2"
    watsonx_explanation_model: str = "ibm/granite-3-8b-instruct"
    
    # External APIs
    nasa_firms_api_url: str = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
    gdelt_api_url: str = "https://api.gdeltproject.org/api/v2/doc/doc"
    
    # Application Settings
    upload_dir: str = "./uploads"
    max_file_size_mb: int = 50
    allowed_extensions: str = "pdf"
    log_level: str = "INFO"
    
    # Computed properties
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size to bytes"""
        return self.max_file_size_mb * 1024 * 1024
    
    @property
    def allowed_extensions_list(self) -> list[str]:
        """Get list of allowed file extensions"""
        return [ext.strip() for ext in self.allowed_extensions.split(",")]


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Dependency injection for FastAPI"""
    return settings

# Made with Bob
