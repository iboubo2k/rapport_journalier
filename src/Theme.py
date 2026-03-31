import streamlit as st

def apply_theme():
    st.markdown(
        """
        <style>
        /* IMPORTANT:
           no background here, so main.py keeps the image on every page
        */
        .stApp {
            color: #FFFFFF;
        }

        h1, h2, h3 {
            color: #FF7900 !important;
            font-weight: 700;
        }

        .stMarkdown, p, span, label, div {
            color: #FFFFFF;
        }

        section[data-testid="stSidebar"] {
            background: rgba(13, 13, 13, 0.92);
            border-right: 2px solid #FF7900;
        }

        div[data-testid="metric-container"] {
            background: rgba(26, 26, 26, 0.88);
            border-left: 6px solid #FF7900;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0 4px 12px rgba(255,121,0,0.35);
        }

        div[data-testid="metric-container"] > div {
            color: #FF7900 !important;
        }

        .stButton > button {
            border-radius: 10px;
            font-weight: bold;
            border: 1px solid #FF7900;
            background: rgba(26, 26, 26, 0.88);
            color: white;
        }

        .stButton > button:hover {
            border: 1px solid #FFA64D;
            color: #FFA64D;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"] > div {
            background-color: rgba(26, 26, 26, 0.88) !important;
            border: 1px solid #FF7900 !important;
            border-radius: 8px;
            color: white !important;
        }

        div[role="radiogroup"] label {
            color: #FF7900 !important;
            font-weight: 600;
        }

        .stDateInput > div,
        .stSelectbox > div,
        .stTextInput > div {
            background-color: transparent !important;
        }

        .stDataFrame {
            background-color: rgba(26, 26, 26, 0.88);
            border: 1px solid #FF7900;
            border-radius: 10px;
        }

        [data-testid="stExpander"] {
            background: rgba(26, 26, 26, 0.80);
            border-radius: 10px;
            border: 1px solid rgba(255,121,0,0.35);
        }

        .block-container {
            background: rgba(0, 0, 0, 0.18);
            border-radius: 16px;
            padding: 1.2rem 1.2rem 2rem 1.2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
