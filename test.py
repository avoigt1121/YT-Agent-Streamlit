import requests
import os
import ssl
import urllib3
# Save the original request method
original_request = requests.Session.request

# Define a new version that always injects verify=False
def patched_request(self, method, url, *args, **kwargs):
    kwargs['verify'] = False
    return original_request(self, method, url, *args, **kwargs)

# Overwrite the session request method with our patched version
requests.Session.request = patched_request
# This bypasses the certificate check globally for this script
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# This handles the 'requests' library specifically (which the scraper uses)
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(category=InsecureRequestWarning)


import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

video_id = "dQw4w9WgXcQ" # Test video
api_key = "0dfdccdd78216beee8cd360ab9ec6d63" # Your ScraperAPI key
proxy_url = f"http://scraperapi:{api_key}@proxy-server.scraperapi.com:8001"
# Standard Requests-style proxy dict
proxies = GenericProxyConfig(
    http_url=proxy_url,
    https_url=proxy_url
)

try:
    print("Attempting to fetch transcript via ScraperAPI...")
    # Passing proxies directly to the library
    ytt_api = YouTubeTranscriptApi(proxy_config=proxies) 
    transcript = ytt_api.fetch(video_id)

    print("Success! Proxy is working.")
    print(transcript[0]) # Print first line
except Exception as e:
    print(f"Still having trouble: {e}")