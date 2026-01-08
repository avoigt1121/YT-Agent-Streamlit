# YouTube Transcript Functions
# Free version without OpenAI dependencies

from youtube_transcript_api import YouTubeTranscriptApi
import re
import urllib.parse
from youtube_transcript_api.proxies import GenericProxyConfig
import os
'''
def fetch_video_transcript_deprecated(url: str) -> str:
    """
    Extract transcript with timestamps from a YouTube video URL
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Formatted transcript with timestamps in format: "[MM:SS] Text"
    """
    # Extract video ID from URL
    video_id_pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11})'
    video_id_match = re.search(video_id_pattern, url)
    if not video_id_match:
        return "Invalid YouTube URL"
    video_id = video_id_match.group(1)

    import requests
    import xml.etree.ElementTree as ET
    import os
    import html
    # ScraperAPI endpoint for YouTube transcript XML
    scraperapi_key = os.environ.get('MY_KEY', '0dfdccdd78216beee8cd360ab9ec6d63')
    transcript_url = f"https://www.youtube.com/api/timedtext?lang=en&v={video_id}"
    payload = {
        'api_key': scraperapi_key,
        'url': transcript_url
    }
    try:
        payload = { 'api_key': '0dfdccdd78216beee8cd360ab9ec6d63', 'url': 'https://www.youtube.com/api/timedtext?lang=en&v=dQw4w9WgXcQ&kind=asr', 'output_format': 'markdown' }
        response = requests.get('https://api.scraperapi.com/', params=payload)

        response.raise_for_status()
        text_response = response.text.strip()
        if not text_response or text_response.lstrip().startswith("<!DOCTYPE html") or text_response.lstrip().startswith("<html"):
            print(response.text)
            return "No transcript available."
        return text_response
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

        '''

def fetch_video_transcript(url):
    def format_transcript(transcript):
        """Format transcript entries with timestamps"""
        formatted_entries = []
        for entry in transcript:
            # Convert seconds to MM:SS format
            minutes = int(entry.start // 60)
            seconds = int(entry.start % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"

            formatted_entry = f"{timestamp} {entry.text}"
            formatted_entries.append(formatted_entry)

        # Join all entries with newlines
        return "\n".join(formatted_entries)
    def extract_video_id(url):
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
        if match:
            return match.group(1)
        return None
    video_id = str(extract_video_id(url))
    # First attempt: Try without proxy
    try:
        scraperapi_key = os.getenv("SCRAPERAPI_KEY") or '0dfdccdd78216beee8cd360ab9ec6d63'
        if scraperapi_key:
            try:
                # CORRECTED: Use the Proxy Port format (User:Pass@Host:Port)
                # Note: We use 'http' even for https targets because the proxy handles the tunnel
                proxy_url = f"http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001"
                
                proxy_config = GenericProxyConfig(
                    http_url=proxy_url,
                    https_url=proxy_url
                )
                
                ytt_api_with_proxy = YouTubeTranscriptApi(proxy_config=proxy_config)
                transcript = ytt_api_with_proxy.fetch(video_id)
                return format_transcript(transcript)
            except Exception as e:
                print(f"Proxy failed: {e}. Falling back to direct connection.")
                # Second attempt: Try without ScraperAPI proxy
                # Note: Standard library uses static methods, but following your class structure:
                ytt_api = YouTubeTranscriptApi() 
                transcript = ytt_api.fetch(video_id)
                return format_transcript(transcript)
    except Exception as proxy_error:
        raise Exception(f"Error fetching transcript (tried with and without proxy): {str(proxy_error)}")
