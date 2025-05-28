import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.config_loader import Config
from src.audio.extract_audio import extract_audio
from src.transcription.transcriber import Transcriber
from src.translation.translator import SubtitleTranslator
from src.subtitles.subtitle_generator import SubtitleGenerator
from src.video_processor.video_processor import burn_subtitles

"""def check_input_file():
    if not os.path.exists(Config.VIDEO_PATH):
        print(f"❌ Error: Input video not found at {Config.VIDEO_PATH}")
        return False
    return True"""

def main(video_path, original_language, final_language):
    # Extract audio
    if not extract_audio(video_path = video_path):
        return
    
    # Transcribe
    transcriber = Transcriber()
    segments = transcriber.transcribe(language = original_language)
    if not segments:
        return
    
    # Translate
    translator = SubtitleTranslator()
    translated_segments = translator.translate_segments(segments, original_language, final_language) 
    if not translated_segments:
        return
    
    # Generate subtitles
    subtitle_gen = SubtitleGenerator()
    if not subtitle_gen.generate_srt(translated_segments):
        return
    
    # Burn subtitles
    if burn_subtitles(video_path = video_path):
        print(f"✅ Done! Output saved as: {Config.OUTPUT_VIDEO_PATH}")
    else:
        print("❌ Failed to process video")

if __name__ == "__main__":
    main()