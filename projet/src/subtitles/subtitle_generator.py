import sys
import os

# Add the parent directory of src to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


import srt
from datetime import timedelta
from src.config.config_loader import Config

class SubtitleGenerator:
    @staticmethod
    def make_srt_segment(seg, idx):
        start = timedelta(seconds=seg["start"])
        end = timedelta(seconds=seg["end"])
        content = f"{seg['text']}\n{seg['translated']}"
        return srt.Subtitle(index=idx, start=start, end=end, content=content)
    
    def generate_srt(self, segments, output_path=Config.SUBTITLE_PATH):
        try:
            subs = [self.make_srt_segment(seg, i + 1) 
                   for i, seg in enumerate(segments)]
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(srt.compose(subs))
            return True
        except Exception as e:
            print(f"Error generating subtitles: {str(e)}")
            return False