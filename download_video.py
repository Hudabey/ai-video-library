import yt_dlp

def download_youtube_video(url, output_path="video.mp4"):
    """Download a YouTube video"""
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': output_path,
        'quiet': False,
    }
    
    print(f"Downloading video from: {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"✅ Video downloaded to: {output_path}")

if __name__ == "__main__":
    # Your YouTube URL
    url = "https://www.youtube.com/shorts/f5v98HS42r8"
    download_youtube_video(url, "test_video.mp4")