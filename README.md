# AI Agents - Streamlit & Hugging Face

A Streamlit application demonstrating AI capabilities using Hugging Face models, containerized with Docker.

## Learning Goals

This project uses:
-Streamlit
-HuggingFace 
-Docker

## Features

- Text Sentiment Analysis
- Text Generation
- Question Answering
- Docker Support
- Clean UI

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Git

## Local Development

### Option 1: Run with Python 

1. **Clone and navigate to the repository**:
   ```bash
   git clone <your-repo-url>
   cd YT-Agent-Streamlit
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and go to `http://localhost:8501`

### Option 2: Run with Docker

1. **Build the Docker image**:
   ```bash
   docker build -t yt-agent-streamlit .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8501:8501 yt-agent-streamlit
   ```

3. **Or use Docker Compose** (easier):
   ```bash
   docker-compose up
   ```

## Project Structure

```
YT-Agent-Streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## How It Works

1. **Streamlit Frontend**: Creates an interactive web interface
2. **Hugging Face Models**: Pre-trained AI models for various tasks:
   - `distilbert-base-uncased-finetuned-sst-2-english` for sentiment analysis
   - `gpt2` for text generation
   - `distilbert-base-cased-distilled-squad` for question answering
3. **Caching**: Models are cached for better performance
4. **Docker**: Containerizes the entire application for easy deployment

## Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [Docker Documentation](https://docs.docker.com/)

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new features
- Improve the documentation
- Fix bugs
- Share your modifications

---

I also used Shaw Talebi's youtube video to help me learn. & his repo for youtube text agent
