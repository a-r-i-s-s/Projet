<<<<<<< HEAD
def process_video():
    pass
=======
import sys
import os

# Add the parent directory of src to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from googletrans import Translator
from src.config.config_loader import Config

class SubtitleTranslator:
    def __init__(self):
        self.translator = Translator()
    
    def translate_segments(self, segments, src=Config.SOURCE_LANG_TRANSLATE, dest=Config.TARGET_LANG):
        try:
            for seg in segments:
                text = seg["text"]
                translation = self.translator.translate(text, src=src, dest=dest).text
                seg["translated"] = translation
            return segments
        except Exception as e:
            print(f"Translation error: {str(e)}")
            return None
>>>>>>> feature/new_branch_remy
