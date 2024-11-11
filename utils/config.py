from dotenv import load_dotenv
import os
from typing import Optional

def load_environment_variables(env_file: Optional[str] = None) -> None:
    """
    Load environment variables from .env file
    
    Args:
        env_file: Optional path to .env file. If None, searches in current directory
    """
    # Load the specified .env file or search in current directory
    load_dotenv(dotenv_path=env_file)

def get_api_key(key_name: str) -> str:
    """
    Get API key from environment variables
    
    Args:
        key_name: Name of the environment variable
        
    Returns:
        str: API key value
        
    Raises:
        ValueError: If API key is not found
    """
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in environment variables")
    return api_key
