#import yaml

import os

class Config:
    # Define base data directory
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # File paths
    VIDEO_PATH = os.path.join(DATA_DIR, "input_video_2.mp4")
    AUDIO_PATH = os.path.join(DATA_DIR, "audio.wav")
    SUBTITLE_PATH = os.path.join(DATA_DIR, "subtitles.srt")
    OUTPUT_VIDEO_PATH = os.path.join(DATA_DIR, "output_video.mp4")
    
    # Other configurations
    WHISPER_MODEL = "tiny"
    SOURCE_LANG_TRANSCRIBE = "zh"
    SOURCE_LANG_TRANSLATE = "zh-cn"
    TARGET_LANG = "en"

"""
def load_config(path="config/default_config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
"""
import yaml

def load_config(path="config/default_config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)