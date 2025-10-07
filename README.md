# 🎥 AI Video Library Search

An intelligent video search engine that lets you search across multiple videos using natural language queries and jump directly to relevant moments.

## ✨ Features

- **🎯 Semantic Search**: Search using natural language - AI understands context, not just keywords
- **📚 Multi-Video Library**: Build your personal video library from YouTube
- **⏱️ Instant Jump**: Click timestamps to jump directly to relevant moments
- **🤖 AI-Powered**: Uses OpenAI's Whisper for transcription and GPT-4 for semantic understanding
- **🎬 Video Playback**: Watch videos directly in the app

## 🚀 How It Works

1. **Add Videos**: Paste a YouTube URL and give it a name
2. **AI Transcription**: Whisper transcribes the entire video with timestamps
3. **Smart Search**: Ask questions in natural language (e.g., "explain machine learning")
4. **Jump to Moments**: Click timestamps to instantly watch that part

## 🛠️ Tech Stack

- **Python** - Core language
- **Streamlit** - Web interface
- **OpenAI Whisper** - Speech-to-text transcription
- **GPT-4** - Semantic search and understanding
- **yt-dlp** - Video downloading

## 📸 Demo

*[Add screenshots here after you take them]*

## 💡 Use Cases

- Search lecture recordings for specific topics
- Find exact moments in tutorial videos
- Navigate long interview recordings
- Build searchable knowledge base from video content

## ⚙️ Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-video-search.git
cd ai-video-search

# Install dependencies
pip install -r requirements.txt

# Add OpenAI API key to .env file
echo "OPENAI_API_KEY=your-key-here" > .env

# Run the app
streamlit run app.py


🔑 Requirements

Python 3.8+
OpenAI API key
~$0.10-0.50 per video for transcription

📝 Note
Built in one evening as a portfolio project to demonstrate AI engineering skills.
