import subprocess

try:
    out = subprocess.run(["ffmpeg", "-version"], check=True, capture_output=True)
    print("✅ FFmpeg is working!")
    print(out.stdout.decode())
except FileNotFoundError:
    print("❌ FFmpeg is STILL not found.")
