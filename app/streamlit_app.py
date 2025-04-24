import streamlit as st

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.translation import translator as tor

st.title("🎥 Traduction automatique vidéo CH ➜ FR")

uploaded_file = st.file_uploader("Dépose une vidéo ici", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    with st.spinner("Traitement en cours..."):
        srt_path = tor.process_video(uploaded_file)
        st.success("Sous-titres générés !")
        st.download_button("⬇️ Télécharger les sous-titres", open(srt_path, "rb"), file_name="subtitles.srt")

