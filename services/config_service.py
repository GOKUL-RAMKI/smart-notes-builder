"""
Configuration service module.

Manages application configuration stored in config.json.
Handles Gemini API key loading and saving with graceful error handling.
"""

import json
from pathlib import Path
from google import genai

# Configuration
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "gemini_api_key": "",
    "gemini_model": "models/gemini-2.5-flash-lite"
}


def _ensure_config_exists() -> None:
    """
    Ensure config.json exists with default structure.
    
    Creates config.json if missing with default empty configuration.
    If file exists but is malformed, it will be recreated on next save.
    
    Raises:
        Exception: If file creation fails due to permission issues
    """
    config_path = Path(CONFIG_FILE)
    
    if not config_path.exists():
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to create config.json: {str(e)}")

def get_available_models():

    api_key = load_api_key()

    client = genai.Client(
        api_key=api_key
    )

    models = []

    for model in client.models.list():

        name = model.name

        if not name.startswith("models/gemini"):
            continue

        if "embedding" in name:
            continue

        if "tts" in name:
            continue

        if "audio" in name:
            continue

        if "live" in name:
            continue

        if "robotics" in name:
            continue

        models.append(name)

    return sorted(models)

def load_api_key() -> str:
    """
    Load Gemini API key from config.json.
    
    Process (Section 25):
    - Ensure config file exists
    - Read config.json
    - Extract gemini_api_key field
    - Return API key or empty string if missing/unconfigured
    
    Handles malformed JSON gracefully by returning empty string.
    
    Returns:
        str: Gemini API key (empty string if not configured or error occurs)
    """
    # Step 1: Ensure config exists
    _ensure_config_exists()
    
    config_path = Path(CONFIG_FILE)
    
    try:
        # Step 2: Read config.json with UTF-8 encoding
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        
        # Step 3: Extract and return API key
        api_key = config_data.get("gemini_api_key", "")
        
        # Step 4: Return empty string if missing or None
        return api_key if api_key else ""
    
    except json.JSONDecodeError:
        # Handle malformed JSON gracefully
        return ""
    except Exception as e:
        # Handle other errors gracefully
        return ""
    
def load_model() -> str:

    _ensure_config_exists()

    try:

        with open(
            CONFIG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            config_data = json.load(f)

        return config_data.get(
            "gemini_model",
            "models/gemini-2.5-flash-lite"
        )

    except Exception:

        return "models/gemini-2.5-flash-lite"

def save_api_key(api_key: str) -> None:
    """
    Save Gemini API key to config.json.
    
    Process (Section 25):
    - Ensure config file exists
    - Read current configuration
    - Update gemini_api_key field
    - Write back to config.json with valid JSON format
    - Preserve UTF-8 encoding
    
    Args:
        api_key: The API key to save (can be empty string)
        
    Raises:
        Exception: If save fails due to permission issues or file errors
    """
    # Step 1: Ensure config exists
    _ensure_config_exists()
    
    try:
        # Step 2: Read current configuration
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config_data = json.load(f)
        except json.JSONDecodeError:
            # If malformed, start fresh with defaults
            config_data = DEFAULT_CONFIG.copy()
        except Exception:
            config_data = DEFAULT_CONFIG.copy()
        
        # Step 3: Update gemini_api_key field
        config_data["gemini_api_key"] = api_key
        
        # Step 4: Write back to config.json with proper formatting
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    except Exception as e:
        raise Exception(f"Failed to save API key: {str(e)}")

def save_model(model_name: str) -> None:

    _ensure_config_exists()

    try:

        try:

            with open(
                CONFIG_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                config_data = json.load(f)

        except Exception:

            config_data = DEFAULT_CONFIG.copy()

        config_data["gemini_model"] = model_name

        with open(
            CONFIG_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                config_data,
                f,
                indent=2,
                ensure_ascii=False
            )

    except Exception as e:

        raise Exception(
            f"Failed to save model: {str(e)}"
        )
