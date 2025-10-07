


import json
import os
from pathlib import Path

class VideoManager:
    def __init__(self, data_dir="video_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.index_file = self.data_dir / "index.json"
        
    def save_transcript(self, video_name, transcript):
        """Save transcript for a video"""
        # Save full transcript object
        video_dir = self.data_dir / video_name
        video_dir.mkdir(exist_ok=True)
        
        transcript_data = {
            "text": transcript.text,
            "segments": [
                {
                    "start": seg.start,
                    "end": seg.end,
                    "text": seg.text
                }
                for seg in transcript.segments
            ]
        }
        
        with open(video_dir / "transcript.json", "w") as f:
            json.dump(transcript_data, f)
            
        # Update index
        self._update_index(video_name)
        
    def _update_index(self, video_name):
        """Update the index of all videos"""
        if self.index_file.exists():
            with open(self.index_file, "r") as f:
                index = json.load(f)
        else:
            index = {"videos": []}
            
        if video_name not in index["videos"]:
            index["videos"].append(video_name)
            
        with open(self.index_file, "w") as f:
            json.dump(index, f)
            
    def get_all_videos(self):
        """Get list of all processed videos"""
        if not self.index_file.exists():
            return []
        with open(self.index_file, "r") as f:
            return json.load(f)["videos"]
            
    def get_transcript(self, video_name):
        """Load transcript for a video"""
        transcript_file = self.data_dir / video_name / "transcript.json"
        if not transcript_file.exists():
            return None
        with open(transcript_file, "r") as f:
            return json.load(f)

