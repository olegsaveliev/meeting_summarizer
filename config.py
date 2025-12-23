"""
Configuration for Meeting Summarizer Agent
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration settings"""
    
    # API Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Settings
    DEFAULT_MODEL = "gpt-3.5-turbo"  # Fast and cheap
    PREMIUM_MODEL = "gpt-4"          # Higher quality
    
    # Temperature (0 = deterministic, 1 = creative)
    TEMPERATURE = 0.3  # Low for consistent formatting
    
    # Token limits
    MAX_INPUT_TOKENS = 6000   # ~4500 words
    MAX_OUTPUT_TOKENS = 2000  # ~1500 words
    
    # Output settings
    OUTPUT_DIR = "output"
    
    # Default output format
    OUTPUT_FORMAT = "markdown"  # markdown, text, json
    
    # Features
    GENERATE_EMAIL = True
    GENERATE_EXEC_BRIEF = False  # Optional, can enable later
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "No API key found! Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file"
            )
        
        # Create output directory if it doesn't exist
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        
        return True

# Validate on import
Config.validate()