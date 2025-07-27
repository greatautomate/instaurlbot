import json
import os
import logging
from typing import Set, List
from config import Config

logger = logging.getLogger(__name__)

class UserDatabase:
    def __init__(self):
        self.db_file = Config.DATABASE_FILE
        self.users: Set[int] = set()
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.users = set(data.get('users', []))
                logger.info(f"Loaded {len(self.users)} users from database")
            else:
                logger.info("Database file not found, starting with empty user list")
        except Exception as e:
            logger.error(f"Error loading users from database: {e}")
            self.users = set()
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            data = {
                'users': list(self.users),
                'total_users': len(self.users)
            }
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Saved {len(self.users)} users to database")
        except Exception as e:
            logger.error(f"Error saving users to database: {e}")
    
    def add_user(self, user_id: int) -> bool:
        """Add a user to the database"""
        if user_id not in self.users:
            self.users.add(user_id)
            self.save_users()
            logger.info(f"Added new user: {user_id}")
            return True
        return False
    
    def remove_user(self, user_id: int) -> bool:
        """Remove a user from the database"""
        if user_id in self.users:
            self.users.remove(user_id)
            self.save_users()
            logger.info(f"Removed user: {user_id}")
            return True
        return False
    
    def get_all_users(self) -> List[int]:
        """Get all users as a list"""
        return list(self.users)
    
    def get_user_count(self) -> int:
        """Get total number of users"""
        return len(self.users)
    
    def is_user_exists(self, user_id: int) -> bool:
        """Check if user exists in database"""
        return user_id in self.users
    
    def clear_users(self):
        """Clear all users (admin only)"""
        self.users.clear()
        self.save_users()
        logger.warning("All users cleared from database")
    
    def get_stats(self) -> dict:
        """Get database statistics"""
        return {
            'total_users': len(self.users),
            'users': list(self.users)
        }
