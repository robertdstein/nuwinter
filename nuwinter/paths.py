"""
This module is used to load the environment variables from the .env file
"""
import logging
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

code_dir = Path(__file__).resolve().parent

env_file = code_dir / ".env"

if env_file.exists():
    logger.info(f"Loading environment variables from {env_file}")
    load_dotenv(dotenv_path=env_file)
else:
    logger.warning(
        f"No .env file found in {code_dir}. "
        f"Make sure to set the environment variables manually."
    )
