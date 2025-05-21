import sys
import os

# Add the parent directory of src to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import subprocess
from src.config.config_loader import Config
import ffmpeg

def burn_subtitles(video_path=Config.VIDEO_PATH, 
                  subtitle_path=Config.SUBTITLE_PATH,
                  output_path=Config.OUTPUT_VIDEO_PATH):
    try:
        # Convert paths to proper format for FFmpeg
        subtitle_path = os.path.abspath(subtitle_path).replace('\\', '/')
        video_path = os.path.abspath(video_path).replace('\\', '/')
        output_path = os.path.abspath(output_path).replace('\\', '/')
        
        # Get video dimensions
        probe = ffmpeg.probe(video_path)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        dimensions = f"{video_info['width']}x{video_info['height']}"
        
        # Build FFmpeg command
        stream = ffmpeg.input(video_path)
        stream = ffmpeg.filter(stream, 'subtitles', 
                             filename=subtitle_path,
                             original_size=dimensions)
        stream = ffmpeg.output(stream, output_path)
        
        # Run FFmpeg
        ffmpeg.run(stream, overwrite_output=True, capture_stderr=True)
        return True
    except ffmpeg.Error as e:
        print(f"Error burning subtitles: {str(e.stderr.decode())}")
        return False