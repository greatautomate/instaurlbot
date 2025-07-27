import logging
import os
import time
from functools import wraps
from typing import Callable, Any
from config import Config

logger = logging.getLogger(__name__)

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
        ]
    )



def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def ensure_directory_exists(directory: str):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created directory: {directory}")

def clean_filename(filename: str) -> str:
    """Clean filename by removing invalid characters"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def admin_only(func: Callable) -> Callable:
    """Decorator to restrict access to admin only"""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        # Get message from args
        message = args[0] if args else None

        if message and hasattr(message, 'from_user'):
            user_id = message.from_user.id
            if user_id != Config.ADMIN_USER_ID:
                await message.reply_text("❌ You don't have permission to use this command.")
                logger.warning(f"Unauthorized admin command attempt by user {user_id}")
                return

        return await func(*args, **kwargs)
    return wrapper

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == Config.ADMIN_USER_ID
