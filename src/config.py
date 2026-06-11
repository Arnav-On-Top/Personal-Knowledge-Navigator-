import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @staticmethod
    def get(key: str, default: str = "") -> str:
        return os.getenv(key, default)
    
    @staticmethod
    def is_debug() -> bool:
        return os.getenv("DEBUG", "false").lower() == "true"

def get_config() -> Config:
    return Config()
