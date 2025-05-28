import sys
import os
os.environ["STREAMLIT_USE_WATCHDOG"] = "false"
sys.modules['torch.classes'] = None


import streamlit as st
import yt_dlp
import tempfile
import requests


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# On l'insère en tête de sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from src.translation import translator as tor
from app.main import main

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


current_dir = os.path.dirname(os.path.abspath(__file__))
 
 
st.title("🎥 Traduction automatique vidéo CH / EN / FR")

language_map = {
    "English": "en",
    "French": "fr",
    "Chinese": "zh-cn"
}

original_language = st.radio(
    "La vidéo est en :",
    ("English", "French", "Chinese")
)

final_language = st.radio(
    "Vous voulez des sous-titres en :",
    ("English", "French", "Chinese")
)
st.write("Original : ", original_language, "/ Final : ", final_language)

original_language = language_map[original_language]
final_language = language_map[final_language]

if original_language != final_language :
        
    uploaded_file = st.file_uploader("Dépose une vidéo ici", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        with st.spinner("Traitement en cours..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name
            main(temp_path, original_language, final_language)
            
            # Add download button for processed video
            output_video_path = os.path.join(project_root, "data", "output_video.mp4")
            if os.path.exists(output_video_path):
                with open(output_video_path, "rb") as file:
                    st.success("Traduction terminée! ✅")
                    st.download_button(
                        label="⬇️ Télécharger la vidéo traduite",
                        data=file,
                        file_name="video_traduite.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("La vidéo traduite n'a pas été générée correctement.")
            
            
    url = st.text_input("Entre l'URL de la vidéo YouTube :")
    
    if url != "":
        # Create temporary file first
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
            # Set up yt-dlp options with the temp file path
            ydl_opts = {
                'noplaylist': True,
                'no_warnings': True,
                'outtmpl': temp_file.name,  # Now temp_file is defined
                'quiet': True
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Download directly to temp file
                    info = ydl.extract_info(url, download=True)
                    temp_path = temp_file.name
                    
                    main(temp_path, original_language, final_language)

                    output_video_path = os.path.join(project_root, "data", "output_video.mp4")
                    if os.path.exists(output_video_path):
                        with open(output_video_path, "rb") as file:
                            st.success("Traduction terminée! ✅")
                            st.video(output_video_path)
                            st.download_button(
                                label="⬇️ Télécharger la vidéo traduite",
                                data=file,
                                file_name="video_traduite.mp4",
                                mime="video/mp4"
                            )
                    else: 
                        st.error("La vidéo traduite n'a pas été générée correctement.")
            
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e).lower()

                if "sign in to confirm" in error_msg or "cookies" in error_msg:
                    st.warning("Échec sans cookies. Tentative avec cookies...")
                
                    cookies_file = st.file_uploader("Importe ton fichier `cookies.txt`", type=['txt'])

                    if not cookies_file:
                        st.error("Cette vidéo nécessite des cookies. Veuillez importer un fichier `cookies.txt`.")
                    else:
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                            tmp.write(cookies_file.read())
                            tmp_path = tmp.name
                        
                        ydl_opts_with_cookies = {
                            'cookiefile': tmp_path,
                            'quiet': True,
                            'noplaylist': True,
                            'outtmpl': '%(title)s.%(ext)s',  # Save with video title as filename
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36',
                            },
                            'ignoreerrors': True
                        }

                        try:
                            with yt_dlp.YoutubeDL(ydl_opts_with_cookies) as ydl:
                                # Download video with cookies
                                info = ydl.extract_info(url, download=True)
                                video_path = ydl.prepare_filename(info)
                                 
                                 # Process the video
                                main(video_path, original_language, final_language)                              
                
                                # Add download button for processed video
                                output_video_path = os.path.join(project_root, "data", "output_video.mp4")
                                if os.path.exists(output_video_path):
                                    with open(output_video_path, "rb") as file:
                                        st.success("Traduction terminée! ✅")
                                        st.video(output_video_path)
                                        st.download_button(
                                            label="⬇️ Télécharger la vidéo traduite",
                                            data=file,
                                            file_name="video_traduite.mp4",
                                            mime="video/mp4"
                                        )
                                else:
                                    st.error("La vidéo traduite n'a pas été générée correctement.")
                                

                        except Exception as e2:
                            st.error("Erreur même avec cookies. Veuilez rafraichir les cookies.")
                            
                    st.markdown("""**Besoin d’aide ?** Utilisez l’extension [Cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) pour exporter vos cookies depuis **FireFox**.""")
                    st.markdown("""**Besoin d’aide ?** Utilisez l’extension [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/lopibhbgjfmmaghejbkojkfjbdhkccme) pour exporter vos cookies depuis **Chrome**.""")
                    
                elif "not a valid url" in error_msg or "invalid" in error_msg:
                    st.error("❌ L'URL fournie est invalide.")
                else:
                    st.error(f"❌ Erreur inconnue. Veuillez vérifier l'URL ou le fichier de cookies.")

# Si on veut lancer l'app et pouvoir mettre des vidéos de 1 Go, il faut lancer avec la commande suivante :
# streamlit run app/streamlit_app.py --server.maxUploadSize=1024

# Ne pas faire attention aux messages d'erreur
# Si ça marche pas, c'est peut-être que la librairie yt-dlp n'est pas à jour
# Pour l'update : pip install -U yt-dlp

# La librairie permet de télécharger, à voir si on peut la traiter sans la download, si on la charge dans un fichier temp, ou en local

