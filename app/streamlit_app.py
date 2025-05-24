import streamlit as st
import yt_dlp
import tempfile

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# On l'insère en tête de sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    
from src.translation import translator as tor
from app.main import main

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


current_dir = os.path.dirname(os.path.abspath(__file__))
 
 
st.title("🎥 Traduction automatique vidéo CH / EN / FR")


original_language = st.radio(
    "La vidéo est en :",
    ("Anglais", "Français", "Chinois")
)

final_language = st.radio(
    "Vous voulez des sous-titres en :",
    ("Anglais", "Français", "Chinois")
)
st.write("Original : ", original_language, "/ Final : ", final_language)



if original_language != final_language :
    
    uploaded_file = st.file_uploader("Dépose une vidéo ici", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        with st.spinner("Traitement en cours..."):
            # Either use the translator
            # srt_path = tor.process_video(uploaded_file)
            # OR capture the return value from main()
            srt_path = main()
            
            if srt_path:  # Add error handling
                st.success("Sous-titres générés !")
                st.download_button("⬇️ Télécharger les sous-titres", 
                                 open(srt_path, "rb"), 
                                 file_name="subtitles.srt")
            else:
                st.error("Erreur lors de la génération des sous-titres")
            
            
    url = st.text_input("Entre l'URL de la vidéo YouTube :")
    
    if url != "":
        
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'noplaylist': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                
                # - - - - - - 
                # Appelle la fonction de traitement vidéo, à modifier 
            
                info = ydl.extract_info(url, download=False)
                st.success("Vidéo analysée sans cookies ✅")
                st.write("**Titre :**", info.get('title'))
                st.write("**Auteur :**", info.get('uploader'))
                st.video(info.get('url'))
            
            
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
                        'skip_download': True,
                        'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36',
                        },
                        'ignoreerrors': True
                    }

                    try:
                        with yt_dlp.YoutubeDL(ydl_opts_with_cookies) as ydl:
                            
                            # - - - - - - 
                            # Appelle la fonction de traitement vidéo, à modifier 
            
                            info = ydl.extract_info(url, download=False)
                            st.success("Vidéo analysée avec cookies ✅")
                            st.write("**Titre :**", info.get('title'))
                            st.write("**Auteur :**", info.get('uploader'))
                            st.video(info.get('url'))

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