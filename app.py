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

# --- LÓGICA DE LOGIN Y SEGURIDAD ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown(f"## {APP_ICON} Bienvenido a {APP_NAME}")
    with st.form("login_form"):
        email_input = st.text_input("Correo electrónico").lower().strip()
        pass_input = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar a la Odisea", type="primary"):
            user = db.get_user(email_input)
            if user and pass_input == user["password"]:
                st.session_state.authenticated = True
                st.session_state.current_user = email_input
                st.session_state.user_rol = user["rol"]
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")
    st.stop()

# --- MODAL DE CAMBIO DE CONTRASEÑA OBLIGATORIO ---
user_data = db.get_user(st.session_state.current_user)
if user_data["password"] == "Itaca2026!":
    st.warning("⚠️ **Seguridad requerida:** Debes cambiar tu contraseña inicial antes de continuar.")
    with st.form("change_password_form"):
        new_pass = st.text_input("Nueva contraseña", type="password", help="Elige algo seguro que solo tú sepas.")
        confirm_pass = st.text_input("Confirma tu nueva contraseña", type="password")
        if st.form_submit_button("Actualizar y Entrar", type="primary"):
            if len(new_pass) < 6:
                st.error("La contraseña debe tener al menos 6 caracteres.")
            elif new_pass != confirm_pass:
                st.error("Las contraseñas no coinciden.")
            elif new_pass == "Itaca2026!":
                st.error("No puedes usar la contraseña inicial.")
            else:
                db.update_password(st.session_state.current_user, new_pass)
                st.success("¡Contraseña actualizada! Bienvenido a bordo.")
                st.balloons()
                st.rerun()
    st.stop() # No deja pasar al resto de la app hasta que cambie la clave


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
