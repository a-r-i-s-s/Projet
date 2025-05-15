import sys
import os

# Add the parent directory of src to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import subprocess
from src.config.config_loader import Config

def burn_subtitles(video_path=Config.VIDEO_PATH, 
                  subtitle_path=Config.SUBTITLE_PATH,
                  output_path=Config.OUTPUT_VIDEO_PATH):
    try:
        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-vf", f"subtitles={subtitle_path}",
            "-c:a", "copy",
            output_path
        ])
        return True
    except Exception as e:
        print(f"Error burning subtitles: {str(e)}")
        return False