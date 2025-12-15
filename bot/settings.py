import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).parent.parent

LOG_CONFIG_FILE = BASE_DIR / ".log-config.yaml"

LOG_FILE = os.getenv("LOG_FILE")