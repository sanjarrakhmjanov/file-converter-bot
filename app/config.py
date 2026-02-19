from dataclasses import dataclass
import os

from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
     bot_token: str

def load_settings() -> Settings:
      load_dotenv()
      token = os.getenv("BOT_TOKEN", "")
      if not token:
           raise RuntimeError("BOT_TOKEN env kerak")
      return Settings(bot_token=token)