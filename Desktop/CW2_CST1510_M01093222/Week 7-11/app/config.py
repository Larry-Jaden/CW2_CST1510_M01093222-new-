"""
Environment configuration loader for the application.
Loads variables from .env files using python-dotenv.
"""

import os
from pathlib import Path
import sys

# Try to import dotenv
try:
    from dotenv import load_dotenv
except ImportError:
    print("python-dotenv is not installed. Install it with: pip install python-dotenv")
    sys.exit(1)

# Load .env file from project root
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
ENV_LOCAL_FILE = PROJECT_ROOT / ".env.local"

# Load local env file first (if exists), then override with .env
if ENV_LOCAL_FILE.exists():
    load_dotenv(ENV_LOCAL_FILE, override=True)
if ENV_FILE.exists():
    load_dotenv(ENV_FILE, override=False)


def get_env(key: str, default=None) -> str:
    """
    Get environment variable with optional default.
    
    Args:
        key: Environment variable name
        default: Default value if key not found
        
    Returns:
        Environment variable value or default
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(f"Environment variable '{key}' not found and no default provided")
    return value


def get_env_optional(key: str, default=None) -> str:
    """
    Get environment variable with optional default (no error if missing).
    
    Args:
        key: Environment variable name
        default: Default value if key not found
        
    Returns:
        Environment variable value or default
    """
    return os.getenv(key, default)
