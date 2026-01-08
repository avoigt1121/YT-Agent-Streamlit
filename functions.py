import requests
import os
import ssl
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# 1. THE MONKEYPATCH
# This forces every 'requests' call to use verify=False
original_request = requests.Session.request
def patched_request(self, method, url, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, method, url, *args, **kwargs)
requests.Session.request = patched_request

# 2. THE GLOBAL SSL BYPASS
# This handles libraries that use 'urllib' instead of 'requests'
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# 3. WARNING SUPPRESSION
# This keeps your console clean of "Insecure Request" warnings
urllib3.disable_warnings(category=InsecureRequestWarning)

# 4. IMPORTS (Now that the environment is patched)
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
import re
import urllib.parse
from dotenv import load_dotenv

# 5. INITIALIZATION
load_dotenv() # Ensure this is called so os.getenv works!
scraperapi_key = os.getenv('SCRAPERAPI_KEY')
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
    try:
        scraperapi_key = os.getenv("SCRAPERAPI_KEY")
        proxy_url = f"http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001"
        proxy_config = GenericProxyConfig(
            http_url=proxy_url,
            https_url=proxy_url
        )
        ytt_api_with_proxy = YouTubeTranscriptApi(proxy_config=proxy_config)
        transcript = ytt_api_with_proxy.fetch(video_id)
        return format_transcript(transcript)

    except Exception as proxy_error:
        raise Exception(f"Error fetching transcript (tried with proxy): {str(proxy_error)}")
