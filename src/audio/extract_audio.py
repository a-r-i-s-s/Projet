from moviepy.editor import VideoFileClip
from src.config.config_loader import Config

def extract_audio(video_path, audio_path=Config.AUDIO_PATH):
    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
        video.close()
        return True
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return False