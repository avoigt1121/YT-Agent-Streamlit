import streamlit as st
from transformers import pipeline
import re
import requests
import json
import os 

my_actual_key = os.environ.get('MY_KEY')

st.set_page_config(page_title="AI Learning Hub", page_icon="🤖", layout="wide")

st.title("AI Learning Hub")
st.sidebar.header("Tools")
tool = st.sidebar.selectbox("Pick a tool:", ["Sentiment", "Text Gen", "Q&A", "YouTube"])

@st.cache_resource
def load_model(task, model_name):
    return pipeline(task, model=model_name)

def get_youtube_transcript(url):
    """Get YouTube transcript using ScraperAPI only (no direct connection)"""
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    
    st.info("🔄 Fetching transcript via ScraperAPI proxy...")
    
    try:
        # Use ScraperAPI to get the YouTube page
        payload = {
            'api_key': '0dfdccdd78216beee8cd360ab9ec6d63',
            'url': url,
            'max_cost': '1'
        }
        response = requests.get('https://api.scraperapi.com/', params=payload)
        
        if response.status_code != 200:
            raise Exception(f"ScraperAPI request failed: {response.status_code}")
        
        html_content = response.text
        
        # Extract transcript from YouTube's embedded JSON data
        transcript_text = extract_transcript_from_html(html_content)
        return transcript_text
        
    except Exception as e:
        raise Exception(f"ScraperAPI transcript extraction failed: {str(e)}")

def extract_transcript_from_html(html_content):
    """Extract transcript from YouTube HTML content"""
    
    # Method 1: Look for ytInitialPlayerResponse
    player_response_pattern = r'var ytInitialPlayerResponse = ({.*?});'
    match = re.search(player_response_pattern, html_content)
    
    if match:
        try:
            player_data = json.loads(match.group(1))
            captions = player_data.get('captions', {}).get('playerCaptionsTracklistRenderer', {})
            caption_tracks = captions.get('captionTracks', [])
            
            if caption_tracks:
                # Get the first available caption track
                caption_url = caption_tracks[0].get('baseUrl')
                if caption_url:
                    return fetch_transcript_from_url(caption_url)
        except:
            pass
    
    # Method 2: Look for alternative patterns
    caption_pattern = r'"captionTracks":\[{"baseUrl":"([^"]+)"'
    match = re.search(caption_pattern, html_content)
    
    if match:
        caption_url = match.group(1).replace('\\u0026', '&')
        return fetch_transcript_from_url(caption_url)
    
    # Method 3: Look for transcript in page data
    transcript_pattern = r'"transcriptRenderer":{"content":"([^"]+)"'
    match = re.search(transcript_pattern, html_content)
    
    if match:
        transcript_content = match.group(1)
        return parse_transcript_content(transcript_content)
    
    raise Exception("No transcript data found in HTML")

def fetch_transcript_from_url(caption_url):
    """Fetch transcript from YouTube's caption URL via ScraperAPI"""
    try:
        payload = {
            'api_key': '0dfdccdd78216beee8cd360ab9ec6d63',
            'url': caption_url,
            'max_cost': '1'
        }
        response = requests.get('https://api.scraperapi.com/', params=payload)
        
        if response.status_code != 200:
            raise Exception(f"Caption URL fetch failed: {response.status_code}")
        
        return parse_xml_transcript(response.text)
        
    except Exception as e:
        raise Exception(f"Failed to fetch caption URL: {str(e)}")

def parse_xml_transcript(xml_content):
    """Parse XML transcript format"""
    # YouTube captions come as XML
    transcript_entries = []
    
    # Extract text elements with start times
    text_pattern = r'<text start="([^"]+)"[^>]*>([^<]+)</text>'
    matches = re.findall(text_pattern, xml_content)
    
    for start_time, text in matches:
        try:
            seconds = float(start_time)
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            timestamp = f"[{minutes:02d}:{secs:02d}]"
            
            # Clean up text (remove HTML entities)
            clean_text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            clean_text = re.sub(r'&#\d+;', '', clean_text)  # Remove numeric entities
            
            transcript_entries.append(f"{timestamp} {clean_text}")
        except:
            continue
    
    if not transcript_entries:
        raise Exception("No transcript entries found in XML")
    
    return '\n'.join(transcript_entries)

def parse_transcript_content(content):
    """Parse transcript content from embedded data"""
    # Decode and clean the content
    content = content.replace('\\n', '\n').replace('\\"', '"')
    
    # Split into lines and format
    lines = content.split('\n')
    formatted_lines = []
    
    for i, line in enumerate(lines):
        if line.strip():
            # Estimate timestamp (rough approximation)
            seconds = i * 3  # Assume ~3 seconds per line
            minutes = seconds // 60
            secs = seconds % 60
            timestamp = f"[{minutes:02d}:{secs:02d}]"
            formatted_lines.append(f"{timestamp} {line.strip()}")
    
    if not formatted_lines:
        raise Exception("No content found to parse")
    
    return '\n'.join(formatted_lines)

if tool == "Sentiment":
    st.header("Sentiment Analysis")
    text = st.text_area("Enter text:")
    if st.button("Analyze") and text:
        model = load_model("sentiment-analysis", "distilbert-base-uncased-finetuned-sst-2-english")
        result = model(text)[0]
        st.metric("Sentiment", result['label'])
        st.metric("Confidence", f"{result['score']:.1%}")

elif tool == "Text Gen":
    st.header("Text Generation") 
    prompt = st.text_input("Enter prompt:")
    length = st.slider("Length:", 20, 100, 50)
    if st.button("Generate") and prompt:
        model = load_model("text-generation", "gpt2")
        result = model(prompt, max_length=length, num_return_sequences=1)[0]
        st.write(result['generated_text'])

elif tool == "Q&A":
    st.header("Question Answering")
    context = st.text_area("Context:")
    question = st.text_input("Question:")
    if st.button("Answer") and context and question:
        model = load_model("question-answering", "distilbert-base-cased-distilled-squad")
        result = model(question=question, context=context)
        st.write(f"**Answer:** {result['answer']}")
        st.write(f"**Confidence:** {result['score']:.1%}")

elif tool == "YouTube":
    st.header("🎬 YouTube Analysis")
    url = st.text_input("YouTube URL:")
    
    if st.button("Get Transcript") and url:
        try:
            transcript = get_youtube_transcript(url)
            st.session_state.transcript = transcript
            st.success("Transcript loaded!")
            st.text_area("Transcript:", transcript[:500] + "...", height=200)
        except Exception as e:
            st.error(f"Error: {e}")
    
    if "transcript" in st.session_state:
        question = st.text_input("Ask about the video:")
        if st.button("Ask") and question:
            model = load_model("question-answering", "deepset/roberta-base-squad2")
            result = model(question=question, context=st.session_state.transcript)
            st.write(f"**Answer:** {result['answer']}")
            st.write(f"**Confidence:** {result['score']:.1%}")
