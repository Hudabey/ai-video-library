import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from video_manager import VideoManager
import yt_dlp

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
vm = VideoManager()

# Page config
st.set_page_config(page_title="AI Video Library", page_icon="🎥", layout="wide")

if 'videos' not in st.session_state:
    st.session_state.videos = vm.get_all_videos()
if 'current_video' not in st.session_state:
    st.session_state.current_video = None
if 'current_time' not in st.session_state:
    st.session_state.current_time = 0
if 'search_results' not in st.session_state:
    st.session_state.search_results = None

def download_video(url, output_name):
    """Download audio and video"""
    os.makedirs(f'video_data/{output_name}', exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio',
        'outtmpl': f'video_data/{output_name}/audio.m4a',
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        
    audio_path = f'video_data/{output_name}/audio.m4a'
    file_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    
    if file_size_mb > 25:
        return None, file_size_mb
    
    video_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': f'video_data/{output_name}/video.mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(video_opts) as ydl:
        ydl.download([url])
    
    return audio_path, file_size_mb

def transcribe_video(audio_path):
    """Transcribe audio file"""
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    return transcript

def search_all_videos(query):
    """Search across all videos"""
    import re
    results = []
    
    for video_name in st.session_state.videos:
        transcript = vm.get_transcript(video_name)
        if not transcript:
            continue
            
        segments_text = "\n".join([
            f"[{seg['start']:.1f}s]: {seg['text']}"
            for seg in transcript['segments']
        ])
        
        prompt = f"""Find top 3 moments about: "{query}"

{segments_text}

List them with EXACT format: [XXs]: description"""
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        matches_text = response.choices[0].message.content
        timestamp_pattern = r'\[(\d+\.?\d*)s\]:\s*(.+?)(?=\[|$)'
        parsed_matches = re.findall(timestamp_pattern, matches_text)
        
        results.append({
            "video": video_name,
            "raw_text": matches_text,
            "timestamps": [(float(t), desc.strip()) for t, desc in parsed_matches]
        })
    
    return results

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .video-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background: #1E1E1E;
        margin: 0.5rem 0;
    }
    .stat-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🎥 AI Video Library</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Search through your video collection using AI-powered semantic search</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📹 Add New Video")
    
    with st.form("add_video_form"):
        video_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")
        video_name = st.text_input("Video Name", placeholder="My Awesome Lecture")
        submit = st.form_submit_button("🚀 Add & Transcribe", use_container_width=True)
        
        if submit and video_url and video_name:
            with st.spinner("⏬ Downloading..."):
                result = download_video(video_url, video_name)
                
            if result[0] is None:
                st.error(f"❌ File too large ({result[1]:.1f} MB). Limit: 25 MB")
            else:
                audio_path, size = result
                st.success(f"✅ Downloaded ({size:.1f} MB)")
                
                with st.spinner("🎯 Transcribing with Whisper AI..."):
                    transcript = transcribe_video(audio_path)
                    vm.save_transcript(video_name, transcript)
                    st.session_state.videos = vm.get_all_videos()
                
                st.success(f"✨ Added {video_name}!")
                st.rerun()
    
    st.divider()
    
    # Stats
    if st.session_state.videos:
        st.metric("Videos in Library", len(st.session_state.videos))

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    # Search
    st.subheader("🔍 Search Your Videos")
    query = st.text_input("", placeholder="What are you looking for? (e.g., 'machine learning basics', 'Python loops')")
    
    if st.button("🔎 Search All Videos", use_container_width=True):
        if not st.session_state.videos:
            st.warning("⚠️ No videos in library yet!")
        elif query:
            with st.spinner("🤔 Searching..."):
                st.session_state.search_results = search_all_videos(query)
        else:
            st.warning("Please enter a search query")

with col2:
    st.subheader("📚 Your Library")
    if st.session_state.videos:
        for video in st.session_state.videos:
            if st.button(f"▶️ {video}", key=f"lib_{video}", use_container_width=True):
                st.session_state.current_video = video
                st.session_state.current_time = 0
                st.rerun()
    else:
        st.info("No videos yet!\nAdd one using the sidebar →")

# Search results
if st.session_state.search_results:
    st.divider()
    st.subheader("🎯 Search Results")
    
    for result in st.session_state.search_results:
        with st.expander(f"📹 **{result['video']}**", expanded=True):
            if result.get('timestamps'):
                for i, (timestamp, description) in enumerate(result['timestamps'], 1):
                    col_time, col_desc = st.columns([1, 5])
                    with col_time:
                        if st.button(f"▶️ {int(timestamp//60)}:{int(timestamp%60):02d}", 
                                   key=f"{result['video']}_{timestamp}_{i}",
                                   use_container_width=True):
                            st.session_state.current_video = result['video']
                            st.session_state.current_time = int(timestamp)
                            st.rerun()
                    with col_desc:
                        st.markdown(f"**{i}.** {description}")
            else:
                st.write(result.get('raw_text', 'No results found'))

# Video player
if st.session_state.current_video:
    st.divider()
    st.subheader(f"▶️ Now Playing: {st.session_state.current_video}")
    
    video_path = f"video_data/{st.session_state.current_video}/video.mp4"
    
    if os.path.exists(video_path):
        st.video(video_path, start_time=st.session_state.current_time)
        
        col_close, col_reset = st.columns([1, 5])
        with col_close:
            if st.button("✕ Close Video"):
                st.session_state.current_video = None
                st.session_state.current_time = 0
                st.rerun()
    else:
        st.error("Video file not found")