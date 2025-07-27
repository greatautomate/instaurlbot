import asyncio
import logging
from typing import List
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, ChatWriteForbidden, PeerIdInvalid
from database import UserDatabase

logger = logging.getLogger(__name__)

class BroadcastManager:
    def __init__(self, app: Client, db: UserDatabase):
        self.app = app
        self.db = db
    
    async def broadcast_message(self, message: str, admin_message: Message) -> dict:
        """Broadcast message to all users"""
        users = self.db.get_all_users()
        total_users = len(users)
        
        if total_users == 0:
            await admin_message.reply_text("❌ No users found in database.")
            return {"success": 0, "failed": 0, "blocked": 0, "total": 0}
        
        # Send confirmation to admin
        status_msg = await admin_message.reply_text(
            f"📢 **Broadcasting message to {total_users} users...**\n\n"
            f"✅ Sent: 0\n"
            f"❌ Failed: 0\n"
            f"🚫 Blocked: 0\n"
            f"📊 Progress: 0/{total_users}"
        )
        
        success_count = 0
        failed_count = 0
        blocked_count = 0
        
        for i, user_id in enumerate(users):
            try:
                await self.app.send_message(user_id, message)
                success_count += 1
                
                # Update status every 10 users or at the end
                if (i + 1) % 10 == 0 or i == total_users - 1:
                    try:
                        await status_msg.edit_text(
                            f"📢 **Broadcasting message to {total_users} users...**\n\n"
                            f"✅ Sent: {success_count}\n"
                            f"❌ Failed: {failed_count}\n"
                            f"🚫 Blocked: {blocked_count}\n"
                            f"📊 Progress: {i + 1}/{total_users}"
                        )
                    except Exception:
                        pass
                
            except FloodWait as e:
                logger.warning(f"FloodWait: {e.value} seconds")
                await asyncio.sleep(e.value)
                try:
                    await self.app.send_message(user_id, message)
                    success_count += 1
                except Exception:
                    failed_count += 1
                    
            except (UserIsBlocked, ChatWriteForbidden):
                blocked_count += 1
                # Remove blocked users from database
                self.db.remove_user(user_id)
                logger.info(f"Removed blocked user {user_id} from database")
                
            except PeerIdInvalid:
                failed_count += 1
                # Remove invalid users from database
                self.db.remove_user(user_id)
                logger.info(f"Removed invalid user {user_id} from database")
                
            except Exception as e:
                failed_count += 1
                logger.error(f"Error sending message to {user_id}: {e}")
            
            # Small delay to avoid hitting rate limits
            await asyncio.sleep(0.1)
        
        # Final status update
        final_message = (
            f"📢 **Broadcast Complete!**\n\n"
            f"✅ Successfully sent: {success_count}\n"
            f"❌ Failed to send: {failed_count}\n"
            f"🚫 Blocked users: {blocked_count}\n"
            f"📊 Total users: {total_users}\n\n"
            f"📈 Success rate: {(success_count/total_users)*100:.1f}%"
        )
        
        try:
            await status_msg.edit_text(final_message)
        except Exception:
            await admin_message.reply_text(final_message)
        
        logger.info(f"Broadcast completed: {success_count} sent, {failed_count} failed, {blocked_count} blocked")
        
        return {
            "success": success_count,
            "failed": failed_count,
            "blocked": blocked_count,
            "total": total_users
        }
    
    async def get_broadcast_stats(self) -> str:
        """Get broadcast statistics"""
        stats = self.db.get_stats()
        return (
            f"📊 **Bot Statistics**\n\n"
            f"👥 Total users: {stats['total_users']}\n"
            f"📅 Database file: {self.db.db_file}\n"
        )
    
    async def send_test_broadcast(self, admin_user_id: int) -> bool:
        """Send test broadcast to admin only"""
        try:
            test_message = (
                "🧪 **Test Broadcast Message**\n\n"
                "This is a test message to verify the broadcast system is working correctly.\n\n"
                "✅ If you receive this message, the broadcast system is functioning properly!"
            )
            
            await self.app.send_message(admin_user_id, test_message)
            return True
        except Exception as e:
            logger.error(f"Error sending test broadcast: {e}")
            return False
