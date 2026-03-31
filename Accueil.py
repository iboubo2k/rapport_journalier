import streamlit as st
from pathlib import Path
import pandas as pd

from src.Theme import apply_theme
from sections import recharge, conso, voix, data_im, data_fixe, sva


PAGE_DATA_FILES = {
    "Recharge": Path("data/recharge_summary.csv"),
    "Conso": Path("data/conso_detail.csv"),
    "Voix": Path("data/voix_detail.csv"),
    "Data IM": Path("data/data_im_detail.csv"),
    "Data Fixe": Path("data/data_fixe_detail.csv"),
    "SVA": Path("data/sva_detail.csv"),
}


def load_bounds_from_file(path: Path):
    if not path or not path.exists():
        return None

    try:
        df = pd.read_csv(path)
    except Exception:
        return None

    date_col = None
    if "Periode" in df.columns:
        date_col = "Periode"
    elif "Date" in df.columns:
        date_col = "Date"

    if date_col is None:
        return None

    dates = pd.to_datetime(df[date_col], errors="coerce").dropna()
    if dates.empty:
        return None

    return dates.min().date(), dates.max().date()


def get_bounds(page=None):
    current_page = page or st.session_state.get("page", "Accueil")

    # La page Accueil n'a pas de dataset propre:
    # on prend Recharge par défaut
    if current_page == "Accueil":
        current_page = "Recharge"

    # 1) essayer le fichier lié à la page courante
    page_file = PAGE_DATA_FILES.get(current_page)
    bounds = load_bounds_from_file(page_file)
    if bounds is not None:
        return bounds

    # 2) fallback utile si la page courante n'a pas encore son fichier
    for fallback_page in ["Recharge", "Conso"]:
        bounds = load_bounds_from_file(PAGE_DATA_FILES.get(fallback_page))
        if bounds is not None:
            return bounds

    today = pd.Timestamp.today().date()
    return today, today


def init_default_dates(force=False):
    min_date, max_date = get_bounds()

    if force or st.session_state.get("date_debut") is None:
        st.session_state.date_debut = min_date

    if force or st.session_state.get("date_fin") is None:
        st.session_state.date_fin = max_date


def switch_page(new_page):
    if st.session_state.get("page") != new_page:
        st.session_state.page = new_page

        # reset des filtres pour que chaque page récupère ses propres bornes
        st.session_state.date_debut = None
        st.session_state.date_fin = None

        init_default_dates(force=True)
        st.rerun()


def render_sidebar():
    init_default_dates()

    with st.sidebar:
        st.markdown("### 🧭 Navigation")

        pages = [
            ("🏠 Accueil", "Accueil"),
            ("💳 Recharge", "Recharge"),
            ("📈 Conso", "Conso"),
            ("📞 Voix", "Voix"),
            ("📡 Data IM", "Data IM"),
            ("🖥 Data Fixe", "Data Fixe"),
            ("⭐ SVA", "SVA"),
        ]

        st.markdown(
            """
            <style>
            .stButton>button {
                width: 100%;
                padding: 0.4em 0;
                text-align: left;
                font-weight: bold;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        for label, page_name in pages:
            if st.button(label, key=f"nav_{page_name}"):
                switch_page(page_name)

        st.markdown("---")
        st.markdown("### ⚙️ Filtres")

        periodicite = st.radio(
            "Périodicité",
            ["Mensuel", "Journalier"],
            index=0 if st.session_state.periodicite == "Mensuel" else 1
        )

        date_debut = st.date_input("Date début", value=st.session_state.date_debut)
        date_fin = st.date_input("Date fin", value=st.session_state.date_fin)

        st.session_state.periodicite = periodicite
        st.session_state.date_debut = date_debut
        st.session_state.date_fin = date_fin

        if date_debut > date_fin:
            st.error("La date de début doit être antérieure à la date de fin.")

        st.markdown("---")

        logo_path = Path("data/logo_orange.png")
        if logo_path.exists():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(str(logo_path), width=120)

        st.markdown(
            """
            **DIRECTION MARKETING**
            DIVISION PILOTAGE DE LA VALEUR ET PLAN MARKETING
            **SERVICE REPORTING & ETUDES**
            📧 thomaszana.coulibaly@orangemali.com
            ☎️ +223 76 29 98 24
            """
        )

        st.markdown("---")

        if st.button("🔒 Déconnexion"):
            st.session_state.clear()
            st.rerun()


def render_home():
    st.title("📊 Rapport Journalier")
    st.subheader("Description de l'application")

    st.markdown(
        """
        Ce dashboard permet de suivre et d’analyser la performance des indicateurs
        sur une période définie par l’utilisateur.

        Il a pour objectif de :
        - suivre le **chiffre d’affaires**
        - visualiser les **évolutions**
        - analyser la contribution des différents **canaux**
        - appliquer des filtres de date par page
        - faciliter l’export des tableaux pour le reporting
        """
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    c1.metric("Page", st.session_state.page)
    c2.metric("Début", str(st.session_state.date_debut))
    c3.metric("Fin", str(st.session_state.date_fin))


def render():
    apply_theme()
    render_sidebar()

    page = st.session_state.page

    if page == "Accueil":
        render_home()
    elif page == "Recharge":
        recharge.render()
    elif page == "Conso":
        conso.render()
    elif page == "Voix":
        voix.render()
    elif page == "Data IM":
        data_im.render()
    elif page == "Data Fixe":
        data_fixe.render()
    elif page == "SVA":
        sva.render()
    else:
        render_home()
