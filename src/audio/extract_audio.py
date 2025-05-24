from moviepy.editor import VideoFileClip
import os
from src.config.config_loader import Config

def extract_audio():
    """Extract audio from video file"""
    try:
        # Debug print to verify paths
        print(f"Extracting audio from: {Config.VIDEO_PATH}")
        print(f"Saving audio to: {Config.AUDIO_PATH}")
        
        # Verify input video exists
        if not os.path.exists(Config.VIDEO_PATH):
            print(f"❌ Input video not found: {Config.VIDEO_PATH}")
            return False
            
        # Load video and extract audio
        video = VideoFileClip(Config.VIDEO_PATH)
        audio = video.audio
        
        if audio is None:
            print("❌ No audio track found in video")
            return False
            
        # Save audio
        audio.write_audiofile(Config.AUDIO_PATH)
        
        # Clean up
        audio.close()
        video.close()
        
        return True
        
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return False