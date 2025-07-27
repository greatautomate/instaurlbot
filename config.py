import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH")
    SESSION_NAME = os.getenv("SESSION_NAME", "instagram_downloader_bot")

    # Admin Configuration
    ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "0"))

    # Instagram API Configuration
    INSTAGRAM_API_URL = "https://api.nekorinn.my.id/downloader/instagram"

    # Bot Configuration
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB limit for Telegram
    DOWNLOAD_TIMEOUT = 30  # seconds

    # Database Configuration
    DATABASE_FILE = "users.json"
    
    # Validate required environment variables
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        if not cls.API_ID or cls.API_ID == 0:
            raise ValueError("API_ID environment variable is required")
        if not cls.API_HASH:
            raise ValueError("API_HASH environment variable is required")
        if not cls.ADMIN_USER_ID or cls.ADMIN_USER_ID == 0:
            raise ValueError("ADMIN_USER_ID environment variable is required")

        return True
