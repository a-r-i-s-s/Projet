import sys
import os

# Add the parent directory of src to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import whisper
except ImportError:
    print("Please install whisper: pip install openai-whisper")

from src.config.config_loader import Config

class Transcriber:
    def __init__(self, model_name=Config.WHISPER_MODEL):
        self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path=Config.AUDIO_PATH, language=Config.SOURCE_LANG_TRANSCRIBE):
        try:
            if(language == "zh-cn"):
                language = "zh"
            result = self.model.transcribe(audio_path, language=language)
            return result["segments"]
        except Exception as e:
            print(f"Transcription error: {str(e)}")
            return None