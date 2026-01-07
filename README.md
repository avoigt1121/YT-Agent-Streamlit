# YT Agent - Learning Streamlit & Hugging Face

A beginner-friendly Streamlit application demonstrating AI capabilities using Hugging Face models, containerized with Docker.

## 🎯 Learning Goals

This project helps you learn:
- **Streamlit**: Building interactive web apps with Python
- **Hugging Face**: Using pre-trained AI models
- **Docker**: Containerizing applications for consistent deployment

## 🚀 Features

- **Text Sentiment Analysis**: Analyze emotions in text
- **Text Generation**: Generate creative content with GPT-2
- **Question Answering**: Ask questions about provided context
- **Docker Support**: Run anywhere with containers
- **Clean UI**: Intuitive interface built with Streamlit

## 📋 Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Git

## 🛠️ Local Development

### Option 1: Run with Python (Recommended for learning)

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

## 📂 Project Structure

```
YT-Agent-Streamlit/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## 🧠 How It Works

1. **Streamlit Frontend**: Creates an interactive web interface
2. **Hugging Face Models**: Pre-trained AI models for various tasks:
   - `distilbert-base-uncased-finetuned-sst-2-english` for sentiment analysis
   - `gpt2` for text generation
   - `distilbert-base-cased-distilled-squad` for question answering
3. **Caching**: Models are cached for better performance
4. **Docker**: Containerizes the entire application for easy deployment

## 🎓 Learning Tips

1. **Start Simple**: Run the app locally first to understand how it works
2. **Explore the Code**: Read through `app.py` to understand the structure
3. **Modify & Experiment**: Try changing the models or adding new features
4. **Docker Learning**: Compare local vs containerized deployment
5. **HuggingFace Hub**: Explore other models at https://huggingface.co/models

## 🔧 Customization Ideas

- Add more Hugging Face models
- Implement file upload functionality
- Add data visualization features
- Create user authentication
- Deploy to cloud platforms (Heroku, Streamlit Cloud, etc.)

## 📚 Resources

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

Happy learning! 🚀
