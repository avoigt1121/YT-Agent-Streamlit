# YouTube Transcript Functions
# Free version without OpenAI dependencies

from youtube_transcript_api import YouTubeTranscriptApi
import re

def fetch_video_transcript(url: str) -> str:
    """
    Extract transcript with timestamps from a YouTube video URL
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Formatted transcript with timestamps in format: "[MM:SS] Text"
    """
    # Extract video ID from URL
    video_id_pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    video_id_match = re.search(video_id_pattern, url)
    
    if not video_id_match:
        raise ValueError("Invalid YouTube URL")
    
    video_id = video_id_match.group(1)
    
    def format_transcript(transcript):
        """Format transcript entries with timestamps"""
        formatted_entries = []
        for entry in transcript:
            start_time = entry.start
            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            timestamp = f"[{minutes:02d}:{seconds:02d}]"
            text = entry.text.strip()
            formatted_entries.append(f"{timestamp} {text}")
        return '\n'.join(formatted_entries)
    
    try:
        # Use fetch method from the API instance
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        return format_transcript(transcript)
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")

