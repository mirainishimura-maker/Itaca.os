"""Centro de Notificaciones"""
import streamlit as st
import database as db
from config import TURQ, GRAY, RED, GREEN, GOLD

def render():
    email = st.session_state.current_user
    st.markdown("## 🔔 Notificaciones")
    notifs = db.get_notificaciones(email, 30)
    if notifs:
        for n in notifs:
            tipo_colors = {"Alerta":RED,"Recordatorio":GOLD,"Faro":TURQ,"Badge":GREEN,"Sistema":GRAY}
            color = tipo_colors.get(n.get("tipo",""), GRAY)
            leida = "opacity:0.6;" if n.get("leida") else ""
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:14px;border-left:4px solid {color};
            box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:8px;{leida}">
                <div style="display:flex;justify-content:space-between;">
                    <span style="font-weight:600;">{n['titulo']}</span>
                    <span style="color:{GRAY};font-size:0.8rem;">{n['fecha'][:16] if n.get('fecha') else ''}</span>
                </div>
                <div style="color:{GRAY};font-size:0.85rem;margin-top:4px;">{n['mensaje']}</div>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No tienes notificaciones.")
