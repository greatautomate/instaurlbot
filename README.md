# Instagram Video Downloader Bot

A Telegram bot that downloads Instagram videos (Reels, Posts, IGTV) using Pyrogram. The bot is designed to handle multiple users simultaneously and can be deployed on Render as a worker service.

## Features

- 🎬 Get Instagram Reels, Posts, and IGTV video download links
- 👥 Support for multiple users simultaneously
- 🚀 Deployable on Render as a worker (no port/health checks needed)
- ⚡ Fast and efficient link extraction using async/await
- 📝 Comprehensive logging and error handling
- 📊 **Video metadata display** (likes, comments, username, caption)
- 🔗 **Direct download links** - no server storage needed
- 📢 **Admin broadcast system** to send messages to all users
- 📊 **User statistics** and database management
- 🔐 **Admin-only commands** with permission control
- 🚫 **No 403 errors** - users download directly from Instagram

## Prerequisites

1. **Telegram Bot Token**: Get it from [@BotFather](https://t.me/BotFather)
2. **Telegram API Credentials**: Get `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org)
3. **Admin User ID**: Your Telegram user ID (get it from [@userinfobot](https://t.me/userinfobot))

## Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd instabot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your credentials:
   ```env
   BOT_TOKEN=your_bot_token_here
   API_ID=your_api_id_here
   API_HASH=your_api_hash_here
   ADMIN_USER_ID=your_telegram_user_id_here
   SESSION_NAME=instagram_downloader_bot
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. **Fork/Clone this repository to your GitHub account**

2. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Set Environment Variables**
   - `BOT_TOKEN`: Your Telegram bot token
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API hash
   - `ADMIN_USER_ID`: Your Telegram user ID

### Method 2: Manual Setup

1. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Choose "Worker" as the service type

2. **Configure Build & Deploy**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

3. **Set Environment Variables**
   - `BOT_TOKEN`: Your Telegram bot token
   - `API_ID`: Your Telegram API ID
   - `API_HASH`: Your Telegram API hash
   - `SESSION_NAME`: `instagram_downloader_bot` (optional)

## Usage

1. **Start the bot**: Send `/start` to your bot
2. **Send Instagram URL**: Copy any Instagram video URL and send it to the bot
3. **Get download links**: The bot will respond with formatted download links and video info
4. **Download video**: Tap the download links to save the video to your device

### Supported URL formats:
- `https://www.instagram.com/reel/ABC123/`
- `https://www.instagram.com/p/ABC123/`
- `https://www.instagram.com/tv/ABC123/`

### Bot Response Format:
When you send an Instagram URL, the bot responds with:
- **Video metadata**: Username, likes, comments, caption
- **Original Instagram URL**: Link back to the original post
- **Direct download links**: Multiple download options
- **Instructions**: How to save the video to your device

**Example Response:**
```
✅ Instagram Video Download Links

👤 User: @username
❤️ Likes: 12,345
💬 Comments: 567
📝 Caption: Amazing video content...

🔗 Original URL:
https://www.instagram.com/reel/ABC123/

📥 Download Links:
1. Download Video 1
2. Download Video 2

💡 How to download:
• Tap any download link above
• Video will open in your browser
• Long press and save to your device

Bot by @medusaXD
```

## Admin Commands

**Note:** Admin commands are only available to the user specified in `ADMIN_USER_ID`.

### Available Admin Commands:

1. **`/broadcast <message>`** - Send a message to all bot users
   ```
   /broadcast Hello everyone! The bot has been updated with new features.
   ```

2. **`/stats`** - View bot statistics
   - Shows total number of users
   - Database information

3. **`/test_broadcast`** - Send a test broadcast message to yourself
   - Useful for testing the broadcast system

### Broadcast Features:
- 📊 **Real-time progress tracking** during broadcast
- 🚫 **Automatic cleanup** of blocked/invalid users
- ⚡ **Rate limiting** to avoid Telegram API limits
- 📈 **Success rate reporting** after broadcast completion
- 🛡️ **Admin-only access** with permission verification

## Project Structure

```
instabot/
├── bot.py              # Main bot file with Pyrogram client
├── config.py           # Configuration and environment variables
├── downloader.py       # Instagram video downloader logic
├── database.py         # User database management
├── broadcast.py        # Broadcast message functionality
├── utils.py            # Utility functions (logging, rate limiting, admin)
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment configuration
├── Procfile           # Process file for deployment
├── runtime.txt        # Python runtime version
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore file
└── README.md          # This file
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Telegram bot token from BotFather |
| `API_ID` | Yes | Telegram API ID from my.telegram.org |
| `API_HASH` | Yes | Telegram API hash from my.telegram.org |
| `ADMIN_USER_ID` | Yes | Telegram user ID of the bot admin |
| `SESSION_NAME` | No | Session name for the bot (default: instagram_downloader_bot) |

### Bot Configuration

- **Max file size**: 50MB (Telegram limit)
- **Download timeout**: 30 seconds
- **Rate limit**: 10 requests per minute per user

## API Used

This bot uses the Instagram downloader API:
- **Endpoint**: `https://api.nekorinn.my.id/downloader/instagram`
- **Method**: GET
- **Parameter**: `url` (Instagram video URL)

## Error Handling

The bot includes comprehensive error handling for:
- Invalid Instagram URLs
- Network timeouts
- File size limits
- API failures
- Telegram API errors (FloodWait, etc.)

## Rate Limiting

- Users are limited to 10 requests per minute
- Prevents API abuse and ensures fair usage

## Logging

The bot logs all important events:
- User interactions
- Download attempts
- Errors and exceptions
- Rate limit violations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Credits

- Bot by @medusaXD
- API provided by @nekorinnn
- Built with [Pyrogram](https://pyrogram.org/)

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
