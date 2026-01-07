import streamlit as st
from transformers import pipeline
import re
from youtube_transcript_api import YouTubeTranscriptApi

st.set_page_config(page_title="AI Learning Hub", page_icon="🤖", layout="wide")

st.title("AI Learning Hub")
st.sidebar.header("Tools")
tool = st.sidebar.selectbox("Pick a tool:", ["Sentiment", "Text Gen", "Q&A", "YouTube"])

@st.cache_resource
def load_model(task, model_name):
    return pipeline(task, model=model_name)

def get_youtube_transcript(url):
    video_id = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")
    
    transcript = YouTubeTranscriptApi.get_transcript(video_id.group(1))
    return '\n'.join([f"[{int(t['start']//60):02d}:{int(t['start']%60):02d}] {t['text']}" for t in transcript])

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
