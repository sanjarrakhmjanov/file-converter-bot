from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
     bot_token: str


def load_settings() -> Settings:
     project_root = Path(__file__).resolve().parent.parent
     dotenv_path = project_root / ".env"
     load_dotenv(dotenv_path=dotenv_path, override=True)
     token = os.getenv("BOT_TOKEN", "")
     if not token:
          raise RuntimeError("BOT_TOKEN env kerak")
     return Settings(bot_token=token)