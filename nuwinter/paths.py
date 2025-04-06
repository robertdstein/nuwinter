"""
This module is used to load the environment variables from the .env file
"""
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

NUWINTER_OUTPUT_DIR = Path(os.environ.get("NUWINTER_DIR", Path.home() / "Data" / "nuwinter"))

logger = logging.getLogger(__name__)

code_dir = Path(__file__).resolve().parent

env_file = code_dir.parent / ".env"

if env_file.exists():
    logger.info(f"Loading environment variables from {env_file}")
    load_dotenv(dotenv_path=env_file)
else:
    logger.warning(
        f"No .env file found in {code_dir}. "
        f"Make sure to set the environment variables manually."
    )


def get_pdf_path(subdir: str) -> Path:
    """
    Function to get the combined candidate pdf for a given night.

    :param subdir: Night to get the combined avro file for.
    :return: File path.
    """
    avro_dir = NUWINTER_OUTPUT_DIR.joinpath(subdir)
    pdf_out_dir = avro_dir.joinpath("winter_candidate_pdf")
    pdf_out_dir.mkdir(parents=True, exist_ok=True)
    out_path = pdf_out_dir.joinpath("combined.pdf")
    return out_path
