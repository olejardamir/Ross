from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables from .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 8000))
    SSL_KEYFILE: str = os.getenv("SSL_KEYFILE", "")
    SSL_CERTFILE: str = os.getenv("SSL_CERTFILE", "")
    RELOAD: bool = os.getenv("RELOAD", "False").lower() in ("true", "1", "yes")

settings = Settings()
