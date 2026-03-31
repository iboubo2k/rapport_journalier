import streamlit as st
import pandas as pd
from pathlib import Path

USER_FILE = Path("data/users.csv")
USER_FILE.parent.mkdir(exist_ok=True)

if not USER_FILE.exists():
    pd.DataFrame(
        columns=["identifiant", "password", "nom", "prenom", "email", "poste"]
    ).to_csv(USER_FILE, index=False)

def load_users():
    return pd.read_csv(USER_FILE)

def check_credentials(identifiant, password):
    df = load_users()
    return not df[
        (df["identifiant"].astype(str) == str(identifiant)) &
        (df["password"].astype(str) == str(password))
    ].empty

def create_account(data):
    df = load_users()
    if str(data["identifiant"]) in df["identifiant"].astype(str).values:
        return False
    df.loc[len(df)] = data
    df.to_csv(USER_FILE, index=False)
    return True

def render():
    st.title("🔐 Connexion au Rapport Journalier")
    st.caption("Authentification obligatoire")

    if not st.session_state.signup_mode:
        with st.form("login_form", clear_on_submit=False):
            identifiant = st.text_input("Identifiant")
            password = st.text_input("Mot de passe", type="password")

            col1, col2, col3 = st.columns(3)
            with col1:
                submit = st.form_submit_button("Connexion", use_container_width=True)
            with col2:
                create = st.form_submit_button("Créer un compte", use_container_width=True)
            with col3:
                quit_btn = st.form_submit_button("Quitter", use_container_width=True)

        if submit:
            if not identifiant or not password:
                st.warning("Veuillez remplir tous les champs.")
            elif check_credentials(identifiant, password):
                st.session_state.logged_in = True
                st.session_state.current_user = identifiant
                st.success(f"Connexion réussie. Bienvenue {identifiant}.")
                st.rerun()
            else:
                st.error("Identifiant ou mot de passe incorrect.")

        if create:
            st.session_state.signup_mode = True
            st.rerun()

        if quit_btn:
            st.info("Fermez simplement l’onglet pour quitter l’application.")

    else:
        with st.form("signup_form"):
            st.subheader("Créer un compte")
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            email = st.text_input("Email professionnel")
            poste = st.text_input("Poste / Fonction")
            identifiant = st.text_input("Identifiant")
            password = st.text_input("Mot de passe (≥ 8 caractères)", type="password")
            confirm = st.text_input("Confirmer le mot de passe", type="password")

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Créer le compte", use_container_width=True)
            with col2:
                back = st.form_submit_button("Retour", use_container_width=True)

        if submit:
            if not all([nom, prenom, email, poste, identifiant, password, confirm]):
                st.warning("Tous les champs sont obligatoires.")
            elif len(password) < 8:
                st.error("Le mot de passe doit contenir au moins 8 caractères.")
            elif password != confirm:
                st.error("Les mots de passe ne correspondent pas.")
            else:
                ok = create_account({
                    "identifiant": identifiant,
                    "password": password,
                    "nom": nom,
                    "prenom": prenom,
                    "email": email,
                    "poste": poste
                })
                if ok:
                    st.success("Compte créé avec succès. Vous pouvez vous connecter.")
                    st.session_state.signup_mode = False
                    st.rerun()
                else:
                    st.error("Cet identifiant existe déjà.")

        if back:
            st.session_state.signup_mode = False
            st.rerun()
