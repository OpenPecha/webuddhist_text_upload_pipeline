"""
Configuration module for Payload Generator Pecha
Handles environment variables and application settings
"""

import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file if it exists
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip loading .env file
    pass


class Config:
    """Configuration class that loads settings from environment variables"""
    
    # API Configuration
    API_BASE_URL: str = os.getenv('WEBUDDHIST_API_BASE_URL', 'https://api.webuddhist.com')
    SEGMENTS_ENDPOINT: str = os.getenv('WEBUDDHIST_SEGMENTS_ENDPOINT', '/api/v1/segments')
    TOC_ENDPOINT: str = os.getenv('WEBUDDHIST_TOC_ENDPOINT', '/api/v1/texts/table-of-content')
    AUTH_ENDPOINT: str = os.getenv('WEBUDDHIST_AUTH_ENDPOINT', '/api/v1/auth/login')
    
    # Authentication (optional - can be provided at runtime)
    EMAIL: Optional[str] = os.getenv('WEBUDDHIST_EMAIL')
    PASSWORD: Optional[str] = os.getenv('WEBUDDHIST_PASSWORD')
    
    # Environment
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def get_full_url(cls, endpoint: str) -> str:
        """Get the full URL for an API endpoint"""
        return f"{cls.API_BASE_URL.rstrip('/')}{endpoint}"
    
    @classmethod
    def get_segments_url(cls) -> str:
        """Get the full URL for segments endpoint"""
        return cls.get_full_url(cls.SEGMENTS_ENDPOINT)
    
    @classmethod
    def get_toc_url(cls) -> str:
        """Get the full URL for table of contents endpoint"""
        return cls.get_full_url(cls.TOC_ENDPOINT)
    
    @classmethod
    def get_auth_url(cls) -> str:
        """Get the full URL for authentication endpoint"""
        return cls.get_full_url(cls.AUTH_ENDPOINT)
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return cls.ENVIRONMENT.lower() == 'production'
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate that required configuration is present"""
        required_vars = [
            'API_BASE_URL',
            'SEGMENTS_ENDPOINT',
            'TOC_ENDPOINT',
            'AUTH_ENDPOINT'
        ]
        
        for var in required_vars:
            if not getattr(cls, var):
                raise ValueError(f"Required configuration variable {var} is not set")
        
        return True


# Create a default config instance
config = Config()

# Validate configuration on import
try:
    config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file or environment variables")
