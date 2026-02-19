"""
⚓ Ítaca OS 2.0
Plataforma Integral de Gestión y Desarrollo Humano
"""
import streamlit as st
import sys
import os
import importlib

# ── CRITICAL: Ensure project root is in Python path ──
# This is the #1 fix for Streamlit Cloud ModuleNotFoundError
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config import APP_NAME, APP_ICON, GLOBAL_CSS
import database as db

# ── PAGE CONFIG ──
st.set_page_config(
    page_title=f"{APP_ICON} {APP_NAME}",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ──
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── INIT DB ──
db.init_db()
# --- LÓGICA DE LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(f"## {APP_ICON} Bienvenido a {APP_NAME}")
    with st.form("login_form"):
        email_input = st.text_input("Correo electrónico")
        pass_input = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar a la Odisea", type="primary"):
            user = db.get_user(email_input)
            if user and pass_input == user["password"]:
                st.session_state.authenticated = True
                st.session_state.current_user = email_input
                st.session_state.user_rol = user["rol"]
                st.success("¡Bienvenido a bordo!")
                st.rerun()
            else:
                st.error("Credenciales incorrectas. Revisa tu correo o contraseña.")
    st.stop() # Detiene la ejecución aquí si no está autenticado

# --- SI ESTÁ AUTENTICADO, MOSTRAR EL RESTO ---
from components.sidebar import render_sidebar
render_sidebar()

# (Aquí sigue el resto de tu código del PAGE ROUTER...)

# ── PAGE ROUTER ──
PAGE_MAP = {
    "Inicio": "pages.home",
    "Mi Esencia": "pages.mi_esencia",
    "Mi Estrategia": "pages.mi_estrategia",
    "Mi Hexágono": "pages.hexagono",
    "Cultura Ítaca": "pages.cultura",
    "Mi Brújula": "pages.brujula",
    "Mis Logros": "pages.logros",
    "Notificaciones": "pages.notificaciones",
    "Admin Dashboard": "pages.admin",
}

page = st.session_state.get("current_page", "Inicio")
module_name = PAGE_MAP.get(page)

if module_name:
    try:
        mod = importlib.import_module(module_name)
        mod.render()
    except Exception as e:
        st.error(f"Error cargando '{page}': {e}")
        import traceback
        st.code(traceback.format_exc())
else:
    st.error(f"Página no encontrada: {page}")
