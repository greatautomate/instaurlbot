import asyncio
import logging
import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageNotModified
from config import Config
from downloader import InstagramDownloader
from utils import setup_logging, admin_only
from database import UserDatabase
from broadcast import BroadcastManager

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

class InstagramBot:
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Initialize Pyrogram client
        self.app = Client(
            Config.SESSION_NAME,
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN
        )
        
        # Initialize downloader
        self.downloader = InstagramDownloader()

        # Initialize database
        self.db = UserDatabase()

        # Initialize broadcast manager
        self.broadcast_manager = BroadcastManager(self.app, self.db)

        # Register handlers
        self.register_handlers()
    
    def register_handlers(self):
        """Register message handlers"""
        
        @self.app.on_message(filters.command("start"))
        async def start_command(client, message: Message):
            await self.handle_start(message)

        @self.app.on_message(filters.command("broadcast"))
        @admin_only
        async def broadcast_command(client, message: Message):
            await self.handle_broadcast(message)

        @self.app.on_message(filters.command("stats"))
        @admin_only
        async def stats_command(client, message: Message):
            await self.handle_stats(message)

        @self.app.on_message(filters.command("test_broadcast"))
        @admin_only
        async def test_broadcast_command(client, message: Message):
            await self.handle_test_broadcast(message)

        @self.app.on_message(filters.text & filters.private)
        async def handle_message(client, message: Message):
            await self.handle_instagram_url(message)
    
    async def handle_start(self, message: Message):
        """Handle /start command"""
        user_id = message.from_user.id

        # Add user to database
        self.db.add_user(user_id)

        welcome_text = (
            "🎬 **Instagram Video Downloader Bot**\n\n"
            "Send me an Instagram video URL (Reel, Post, or IGTV) and I'll download it for you!\n\n"
            "**Supported formats:**\n"
            "• Instagram Reels\n"
            "• Instagram Posts with videos\n"
            "• IGTV videos\n\n"
            "**How to use:**\n"
            "1. Copy an Instagram video URL\n"
            "2. Send it to me\n"
            "3. Wait for the download to complete\n\n"
            "Bot by @medusaXD"
        )

        await message.reply_text(welcome_text)
        logger.info(f"Start command used by user {user_id}")
    
    async def handle_broadcast(self, message: Message):
        """Handle /broadcast command"""
        # Extract message text after command
        command_parts = message.text.split(' ', 1)
        if len(command_parts) < 2:
            await message.reply_text(
                "📢 **Broadcast Command Usage:**\n\n"
                "`/broadcast <your message>`\n\n"
                "**Example:**\n"
                "`/broadcast Hello everyone! The bot has been updated with new features.`\n\n"
                "**Other commands:**\n"
                "• `/stats` - View bot statistics\n"
                "• `/test_broadcast` - Send test message to yourself"
            )
            return

        broadcast_message = command_parts[1]

        # Start broadcast immediately (admin command)
        await self.broadcast_manager.broadcast_message(broadcast_message, message)

    async def handle_stats(self, message: Message):
        """Handle /stats command"""
        stats_text = await self.broadcast_manager.get_broadcast_stats()
        await message.reply_text(stats_text)

    async def handle_test_broadcast(self, message: Message):
        """Handle /test_broadcast command"""
        success = await self.broadcast_manager.send_test_broadcast(message.from_user.id)
        if success:
            await message.reply_text("✅ Test broadcast sent successfully!")
        else:
            await message.reply_text("❌ Failed to send test broadcast.")

    async def handle_instagram_url(self, message: Message):
        """Handle Instagram URL messages"""
        user_id = message.from_user.id
        text = message.text.strip()

        # Add user to database if not exists
        self.db.add_user(user_id)
        
        # Skip if message is a command
        if text.startswith('/'):
            return

        # Check if message contains Instagram URL
        if not self.downloader.is_valid_instagram_url(text):
            await message.reply_text(
                "❌ Please send a valid Instagram URL.\n\n"
                "**Examples:**\n"
                "• https://www.instagram.com/reel/ABC123/\n"
                "• https://www.instagram.com/p/ABC123/\n"
                "• https://www.instagram.com/tv/ABC123/"
            )
            return
        
        # Send processing message
        processing_msg = await message.reply_text("🔄 Processing your request...")
        
        try:
            # Get video information
            video_info = await self.downloader.process_instagram_url(text)
            
            if not video_info or not video_info.get('urls'):
                await processing_msg.edit_text(
                    "❌ Failed to fetch video information. Please check the URL and try again."
                )
                return
            
            # Get video URLs and metadata
            video_urls = video_info['urls']
            metadata = video_info.get('metadata', {})
            original_url = video_info.get('original_url', text)

            if not video_urls:
                await processing_msg.edit_text("❌ No video found in the provided URL.")
                return

            # Format the response message
            response_text = "✅ **Instagram Video Download Links**\n\n"

            # Add metadata if available
            if metadata:
                if metadata.get('username'):
                    response_text += f"👤 **User:** @{metadata['username']}\n"
                if metadata.get('like'):
                    response_text += f"❤️ **Likes:** {metadata['like']:,}\n"
                if metadata.get('comment'):
                    response_text += f"💬 **Comments:** {metadata['comment']:,}\n"
                if metadata.get('caption'):
                    caption = metadata['caption'][:100] + "..." if len(metadata['caption']) > 100 else metadata['caption']
                    response_text += f"📝 **Caption:** {caption}\n"
                response_text += "\n"

            # Add original Instagram URL
            response_text += f"🔗 **Original URL:**\n{original_url}\n\n"

            # Add download URLs
            response_text += "📥 **Download Links:**\n"
            for i, video_url in enumerate(video_urls, 1):
                response_text += f"**{i}.** [Download Video {i}]({video_url})\n"

            response_text += "\n💡 **How to download:**\n"
            response_text += "• Tap any download link above\n"
            response_text += "• Video will open in your browser\n"
            response_text += "• Long press and save to your device\n\n"
            response_text += "Bot by @medusaXD"

            # Send the formatted response
            await processing_msg.edit_text(
                response_text,
                disable_web_page_preview=True
            )

            logger.info(f"Successfully processed Instagram URL for user {user_id}")

        except Exception as e:
            logger.error(f"Error processing Instagram URL: {e}")
            try:
                await processing_msg.edit_text(
                    "❌ An error occurred while processing your request. Please try again later."
                )
            except MessageNotModified:
                pass
    
    async def run(self):
        """Start the bot"""
        logger.info("Starting Instagram Downloader Bot...")
        await self.app.start()
        logger.info("Bot started successfully!")
        
        # Keep the bot running
        await asyncio.Event().wait()

async def main():
    """Main function"""
    bot = InstagramBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())
