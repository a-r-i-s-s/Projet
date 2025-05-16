#script not tested yet

try:
    import whisper
except ImportError:
    print("The 'whisper' module could not be resolved. Ensure it is installed by running 'pip install openai-whisper'.")
from moviepy.editor import VideoFileClip
from googletrans import Translator
import srt
from datetime import timedelta
import subprocess

# --- STEP 1: Extract Audio from Video ---
video_path = "input_video.mp4"
audio_path = "audio.wav"

video = VideoFileClip(video_path)
video.audio.write_audiofile(audio_path)

# --- STEP 2: Transcribe Using Whisper ---
model = whisper.load_model("tiny")  # or "medium"/"large" for better results
result = model.transcribe(audio_path, language='zh')

segments = result["segments"]

# --- STEP 3: Translate CN to EN ---
translator = Translator()
for seg in segments:
    cn = seg["text"]
    en = translator.translate(cn, src='zh-cn', dest='en').text
    seg["translated"] = en

# --- STEP 4: Generate SRT ---
def make_srt_segment(seg, idx):
    start = timedelta(seconds=seg["start"])
    end = timedelta(seconds=seg["end"])
    content = f"{seg['text']}\n{seg['translated']}"
    return srt.Subtitle(index=idx, start=start, end=end, content=content)

subs = [make_srt_segment(seg, i + 1) for i, seg in enumerate(segments)]

with open("subtitles.srt", "w", encoding="utf-8") as f:
    f.write(srt.compose(subs))

# --- STEP 5: Burn Subtitles into Video ---
output_video_path = "output_video.mp4"
subprocess.run([
    "ffmpeg",
    "-i", video_path,
    "-vf", "subtitles=subtitles.srt",
    "-c:a", "copy",
    output_video_path
])

print("✅ Done! Output saved as:", output_video_path)
