import streamlit as st
from transformers import pipeline
import re
import requests
import json
import os
from functions import fetch_video_transcript

st.set_page_config(page_title="AI Learning Hub", layout="wide")

# AI Pipeline Loading
@st.cache_resource
def load_model(task, model_name):
    return pipeline(task, model=model_name)
# Main app
st.title("AI Learning Hub")
st.sidebar.header("Tools")
tool = st.sidebar.selectbox("Pick a tool:", ["Sentiment", "Text Gen", "Q&A", "YouTube"])

if tool == "Sentiment":
    st.header("Sentiment Analysis")
    text = st.text_area("Enter text to analyze:", "I love learning")
    
    if st.button("Analyze Sentiment"):
        model = load_model("sentiment-analysis", "distilbert-base-uncased-finetuned-sst-2-english")
        with st.spinner("Analyzing..."):
            result = model(text)[0]
            st.metric("Sentiment", result['label'])
            st.metric("Confidence", f"{result['score']:.1%}")

elif tool == "Text Gen":
    st.header("Text Generation")
    prompt = st.text_input("Enter prompt:", "The future of AI is")
    length = st.slider("Max length:", 50, 200, 100)
    
    if st.button("Generate Text"):
        model = load_model("text-generation", "gpt2")
        with st.spinner("Generating..."):
            result = model(prompt, max_length=length, num_return_sequences=1)[0]
            st.write(result['generated_text'])

elif tool == "Q&A":
    st.header("Question Answering")
    context = st.text_area("Context:", "HuggingFace is a company that creates AI tools.")
    question = st.text_input("Question:", "What does HuggingFace do?")
    
    if st.button("Get Answer"):
        model = load_model("question-answering", "distilbert-base-cased-distilled-squad")
        with st.spinner("Finding answer..."):
            result = model(question=question, context=context)
            st.write(f"**Answer:** {result['answer']}")
            st.write(f"**Confidence:** {result['score']:.1%}")

elif tool == "YouTube":
    st.header("YouTube Video Analysis")
    
    # Initialize session state for transcript
    if 'transcript' not in st.session_state:
        st.session_state.transcript = None
    
    video_url = st.text_input("YouTube URL:", "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    if st.button("Get Transcript"):
        try:
            with st.spinner("Extracting transcript..."):
                transcript = fetch_video_transcript(video_url)
                st.session_state.transcript = transcript
                st.text_area("Transcript:", transcript, height=200)
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Q&A on transcript
    if st.session_state.transcript:
        st.subheader("Ask Questions About This Video")
        question = st.text_input("Your question:", "What is this video about?", key="youtube_q")
        
        if st.button("Ask", key="youtube_ask"):
            model = load_model("question-answering", "distilbert-base-cased-distilled-squad")
            with st.spinner("Finding answer..."):
                result = model(question=question, context=st.session_state.transcript)
                st.write(f"**Answer:** {result['answer']}")
                st.write(f"**Confidence:** {result['score']:.1%}")

st.markdown("---")
st.markdown("Built with Streamlit, HuggingFace & ScraperAPI")
