from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

LOG_CONFIG_FILE = BASE_DIR / ".log-config.yaml"

LOG_FILE = BASE_DIR / "logs/bot.log"