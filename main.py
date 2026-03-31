import streamlit as st
from pathlib import Path
import base64
import login
import Accueil

st.set_page_config(
    page_title="Rapport Journalier",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_global_image():
    # change the order if you want another image first
    possible_paths = [
        Path("data/img2.jpg"),
        Path("/content/rapport_journalier/data/img2.jpg"),
        Path("/content/banniere.png"),
        Path("/content/rapport_journalier/banniere.png"),
        Path("/content/rapport_journalier/assets/banniere.png"),
    ]

    for img_path in possible_paths:
        if img_path.exists():
            suffix = img_path.suffix.lower()
            mime = "image/png" if suffix == ".png" else "image/jpeg"
            encoded = base64.b64encode(img_path.read_bytes()).decode()

            st.markdown(
                f"""
                <style>
                .stApp {{
                    background:
                        linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.55)),
                        url("data:{mime};base64,{encoded}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )
            return

# -------- Session state --------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

if "periodicite" not in st.session_state:
    st.session_state.periodicite = "Mensuel"

if "date_debut" not in st.session_state:
    st.session_state.date_debut = None

if "date_fin" not in st.session_state:
    st.session_state.date_fin = None

if "signup_mode" not in st.session_state:
    st.session_state.signup_mode = False

# -------- Global image for all pages --------
apply_global_image()

# -------- Routing --------
if st.session_state.logged_in:
    Accueil.render()
else:
    login.render()
