import aiohttp
import re
import logging
from typing import Optional, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class InstagramDownloader:
    def __init__(self):
        self.api_url = Config.INSTAGRAM_API_URL
        self.timeout = Config.DOWNLOAD_TIMEOUT
        self.max_file_size = Config.MAX_FILE_SIZE
    
    def is_valid_instagram_url(self, url: str) -> bool:
        """Check if the provided URL is a valid Instagram URL"""
        instagram_patterns = [
            r'https?://(?:www\.)?instagram\.com/(?:p|reel|tv)/[\w-]+/?',
            r'https?://(?:www\.)?instagram\.com/[\w.-]+/(?:p|reel|tv)/[\w-]+/?'
        ]
        
        for pattern in instagram_patterns:
            if re.match(pattern, url):
                return True
        return False
    
    async def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information from Instagram API"""
        try:
            params = {'url': url}
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.api_url, 
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('status') and data.get('result'):
                            return data['result']
                    else:
                        logger.error(f"API request failed with status {response.status}")
                        return None
                        
        except aiohttp.ClientError as e:
            logger.error(f"Network error while fetching video info: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while fetching video info: {e}")
            return None
    

    
    async def process_instagram_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Process Instagram URL and return video information"""
        if not self.is_valid_instagram_url(url):
            return None

        video_info = await self.get_video_info(url)
        if not video_info:
            return None

        # Handle multiple possible API response formats
        download_urls = []

        # Try different possible field names for video URLs
        possible_url_fields = ['downloadUrl', 'url', 'download_url', 'video_url', 'urls']

        for field in possible_url_fields:
            if field in video_info:
                urls = video_info[field]
                if isinstance(urls, list) and urls:
                    download_urls = urls
                    break
                elif isinstance(urls, str) and urls:
                    download_urls = [urls]
                    break

        # If no URLs found, log the response structure for debugging
        if not download_urls:
            logger.error(f"No video URLs found in API response. Response structure: {video_info}")
            return None

        return {
            'urls': download_urls,
            'metadata': video_info.get('metadata', {}),
            'original_url': url
        }
    

