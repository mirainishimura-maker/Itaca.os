"""Sidebar navigation component - Production version with auth"""
import streamlit as st
from config import APP_NAME, APP_ICON, TURQ, TURQ_DARK
import database as db


def render_sidebar():
    with st.sidebar:
        st.markdown(f"## {APP_ICON} {APP_NAME}")
        st.caption("Plataforma de Gestión y Desarrollo Humano")
        st.divider()

        # ── Usuario autenticado (viene del login en app.py) ──
        email = st.session_state.get("current_user", "")
        user = db.get_user(email)
        identidad = db.get_identidad(email)

        if not user:
            st.error("Usuario no encontrado.")
            return

        rol = user["rol"]
        nombre = user["nombre"]
        st.session_state.user_rol = rol
        st.session_state.user_name = nombre
        st.session_state.user_data = identidad

        # ── Tarjeta de usuario ──
        unidad = user.get("unidad", "")
        st.markdown(f"**👤 {nombre}**")
        st.caption(f"{rol} · {unidad}")

        # ── DISC si tiene ──
        disc = identidad.get("arquetipo_disc") if identidad else None
        if disc:
            from config import DISC_TYPES
            d = DISC_TYPES.get(disc, {})
            st.markdown(f"**DISC:** {d.get('emoji', '')} {disc}")

        # ── Puntos y notificaciones ──
        puntos = db.get_total_puntos(email)
        unread = db.count_unread(email)
        st.markdown(f"**⭐ Puntos:** {puntos}")
        if unread:
            st.markdown(f"**🔔 Notificaciones:** {unread} nueva{'s' if unread > 1 else ''}")

        st.divider()

        # ── Navegación por rol ──
        pages = [
            ("🏠", "Inicio", True),
            ("👤", "Mi Esencia", True),
            ("🎯", "Mi Estrategia", True),
            ("🧭", "Mi Hexágono", rol in ["Admin", "Líder", "Coordinador"]),
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
                is_active = st.session_state.current_page == name
                if st.button(label, key=f"nav_{name}", use_container_width=True,
                             type="primary" if is_active else "secondary"):
                    st.session_state.current_page = name
                    st.rerun()

        st.divider()
        st.caption("v2.0 · Odisea 2026")

        # ── Cerrar sesión ──
        st.divider()
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.current_user = ""
            st.session_state.current_page = "Inicio"
            st.rerun()
