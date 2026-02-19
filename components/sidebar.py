"""Sidebar navigation component"""
import streamlit as st
from config import APP_NAME, APP_ICON, TURQ, TURQ_DARK
import database as db

def render_sidebar():
    with st.sidebar:
        st.markdown(f"## {APP_ICON} {APP_NAME}")
        st.caption("Plataforma de Gestión y Desarrollo Humano")
        st.divider()

        # User selector (en producción sería auth real)
        users = db.get_all_users()
        emails = [u["email"] for u in users]
        names = [f"{u['nombre']} ({u['rol']})" for u in users]
        
        if "current_user" not in st.session_state:
            st.session_state.current_user = emails[0] if emails else ""
        
        idx = emails.index(st.session_state.current_user) if st.session_state.current_user in emails else 0
        selected = st.selectbox("👤 Sesión como:", names, index=idx, key="user_select")
        st.session_state.current_user = emails[names.index(selected)]
        
        user = db.get_user(st.session_state.current_user)
        identidad = db.get_identidad(st.session_state.current_user)
        rol = user["rol"] if user else "Colaborador"
        st.session_state.user_rol = rol
        st.session_state.user_name = user["nombre"] if user else ""
        st.session_state.user_data = identidad
        
        disc = identidad.get("arquetipo_disc") if identidad else None
        if disc:
            from config import DISC_TYPES
            d = DISC_TYPES.get(disc, {})
            st.markdown(f"**DISC:** {d.get('emoji','')} {disc}")
        
        puntos = db.get_total_puntos(st.session_state.current_user)
        unread = db.count_unread(st.session_state.current_user)
        st.markdown(f"**⭐ Puntos:** {puntos}")
        if unread:
            st.markdown(f"**🔔 Notificaciones:** {unread} nueva{'s' if unread>1 else ''}")
        
        st.divider()
        
        # Navigation
        pages = [
            ("🏠", "Inicio", True),
            ("👤", "Mi Esencia", True),
            ("🎯", "Mi Estrategia", True),
            ("🧭", "Mi Hexágono", rol in ["Admin","Líder","Coordinador"]),
            ("❤️", "Cultura Ítaca", True),
            ("🧠", "Mi Brújula", True),
            ("🏆", "Mis Logros", True),
            ("🔔", "Notificaciones", True),
            ("📊", "Admin Dashboard", rol == "Admin"),
        ]
        
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Inicio"
        
        for icon, name, visible in pages:
            if visible:
                label = f"{icon} {name}"
                if name == "Notificaciones" and unread:
                    label += f" ({unread})"
                if st.button(label, key=f"nav_{name}", use_container_width=True,
                           type="primary" if st.session_state.current_page == name else "secondary"):
                    st.session_state.current_page = name
                    st.rerun()
        
        st.divider()
        st.caption(f"v2.0 · Odisea 2026")
