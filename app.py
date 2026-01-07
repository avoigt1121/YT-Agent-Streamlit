import streamlit as st
from transformers import pipeline
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Learning Streamlit & HuggingFace",
    page_icon="🤖",
    layout="wide"
)

# Title and description
st.title("AI Learning Platform")
st.markdown("Learning to use AI Models is easy! This app demonstrates Streamlit with Hugging Face models.")

# Sidebar for navigation
st.sidebar.header("🛠️ Tools")
selected_tool = st.sidebar.selectbox(
    "Choose a tool:",
    ["Text Analysis", "Text Generation", "Question Answering"]
)

# Cache the model loading to improve performance
@st.cache_resource
def load_sentiment_model():
    """Load sentiment analysis model"""
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")  # type: ignore

@st.cache_resource
def load_qa_model():
    """Load question answering model"""
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

@st.cache_resource
def load_text_generation_model():
    """Load text generation model"""
    return pipeline("text-generation", model="gpt2")

# Main content based on selection
if selected_tool == "Text Analysis":
    st.header("Text Sentiment Analysis")
    st.markdown("Analyze the sentiment of your text using a pre-trained Hugging Face model.")
    
    # Text input
    user_input = st.text_area("Enter your text:", placeholder="Type something here...")
    
    if st.button("Analyze Sentiment") and user_input:
        with st.spinner("Analyzing..."):
            try:
                # Load model and analyze
                sentiment_pipeline = load_sentiment_model()
                result = sentiment_pipeline(user_input)
                
                # Display results
                st.success("Analysis Complete!")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Sentiment", result[0]['label'])
                
                with col2:
                    confidence = round(result[0]['score'] * 100, 2)
                    st.metric("Confidence", f"{confidence}%")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif selected_tool == "Text Generation":
    st.header("Text Generation")
    st.markdown("Generate creative text using GPT-2 model.")
    
    prompt = st.text_input("Enter a prompt:", placeholder="Once upon a time...")
    max_length = st.slider("Max length:", 20, 100, 50)
    
    if st.button("Generate Text") and prompt:
        with st.spinner("Generating..."):
            try:
                generator = load_text_generation_model()
                result = generator(prompt, max_length=max_length, num_return_sequences=1)
                
                st.success("Text Generated!")
                st.write("**Generated Text:**")
                st.write(result[0]['generated_text'])
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

elif selected_tool == "Question Answering":
    st.header("Question Answering")
    st.markdown("Ask questions about a given context using BERT.")
    
    context = st.text_area("Context:", placeholder="Provide some context here...")
    question = st.text_input("Question:", placeholder="What would you like to know?")
    
    if st.button("Get Answer") and context and question:
        with st.spinner("Finding answer..."):
            try:
                qa_pipeline = load_qa_model()
                result = qa_pipeline(question=question, context=context)
                
                st.success("Answer Found!")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Answer:**")
                    st.write(result['answer']) # type: ignore
                
                with col2:
                    confidence = round(result['score'] * 100, 2) # type: ignore
                    st.metric("Confidence", f"{confidence}%")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("🚀 Built with Streamlit & Hugging Face | Learning Docker & AI")
