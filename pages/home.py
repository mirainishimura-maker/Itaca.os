"""Módulo HOME - Dashboard Principal"""
import streamlit as st
from datetime import datetime
import database as db
from config import *
from components.cards import metric_card, faro_card, checkin_card, info_card

def render():
    user = st.session_state.get("user_data", {})
    email = st.session_state.current_user
    nombre = user.get("nombre", "Marinero") if user else "Marinero"
    rol = st.session_state.get("user_rol", "Colaborador")

    # Saludo
    hora = datetime.now().hour
    saludo = "Buenos días" if hora < 12 else "Buenas tardes" if hora < 18 else "Buenas noches"
    st.markdown(f"### {saludo}, {nombre.split()[0]}! 👋")

    # Odisea Progress
    ola = get_ola_actual()
    progreso = get_progreso_odisea()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {TURQ_DARK}, {TURQ});border-radius:16px;padding:20px;color:white;margin-bottom:20px;">
        <div style="font-size:0.9rem;opacity:0.9;">⚓ ODISEA 2026 · {ola['emoji']} {ola['nombre']}</div>
        <div style="font-size:1.3rem;font-weight:700;margin:8px 0;">{ola['tema']}</div>
        <div style="background:rgba(255,255,255,0.25);border-radius:8px;height:12px;margin-top:12px;">
            <div style="background:white;width:{progreso}%;height:100%;border-radius:8px;transition:width 1s;"></div>
        </div>
        <div style="font-size:0.8rem;opacity:0.8;margin-top:6px;">{progreso}% del viaje completado</div>
    </div>""", unsafe_allow_html=True)

    # CTAs
    col1, col2 = st.columns(2)
    done = db.checkin_done_this_week(email)
    with col1:
        if done:
            st.success("✅ Check-in hecho esta semana")
        else:
            if st.button("🗣️ HACER CHECK-IN", use_container_width=True, type="primary"):
                st.session_state.current_page = "Cultura Ítaca"
                st.session_state.cultura_tab = "Check-in"
                st.rerun()
    with col2:
        if st.button("🔦 ENVIAR FARO", use_container_width=True):
            st.session_state.current_page = "Cultura Ítaca"
            st.session_state.cultura_tab = "Faros"
            st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Mi Journal", use_container_width=True):
            st.session_state.current_page = "Mi Brújula"
            st.rerun()
    with col2:
        if st.button("🎯 Mis Metas", use_container_width=True):
            st.session_state.current_page = "Mi Estrategia"
            st.rerun()

    st.divider()

    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    puntos = db.get_total_puntos(email)
    logros = db.get_my_logros(email)
    checkins = db.get_my_checkins(email, 4)
    with col1:
        metric_card("⭐ Puntos", puntos)
    with col2:
        metric_card("🏆 Logros", len(logros))
    with col3:
        ultimo_estres = checkins[0]["nivel_estres"] if checkins else "—"
        metric_card("💙 Estrés", f"{ultimo_estres}/5")

    # Widgets de líder
    if rol in ["Admin", "Líder", "Coordinador"]:
        st.markdown("#### ⛵ Tu Tripulación")
        team_checkins = db.get_team_checkins(email)
        if team_checkins:
            avg = sum(c["nivel_estres"] for c in team_checkins[:10]) / min(len(team_checkins), 10)
            pulso = round(10 - avg * 2, 1)
            estado = "🟢 Alta moral" if pulso >= 7 else "🟡 Moderada" if pulso >= 5 else "🔴 Necesita atención"
            col1, col2 = st.columns(2)
            with col1:
                metric_card("Pulso del Equipo", f"{pulso}/10", estado, GREEN if pulso >= 7 else YELLOW if pulso >= 5 else RED)
            with col2:
                metric_card("Check-ins Equipo", f"{len(set(c['email'] for c in team_checkins if c['fecha'][:10] >= (datetime.now().strftime('%Y-%m-%d'))))} esta semana")
        st.divider()

    # Muro de faros
    st.markdown("#### 🔦 Faros Recientes")
    faros = db.get_faros_publicos(5)
    if faros:
        for f in faros[:3]:
            faro_card(f)
        if len(faros) > 3:
            if st.button("Ver todos los faros →"):
                st.session_state.current_page = "Cultura Ítaca"
                st.rerun()
    else:
        st.info("Aún no hay faros. ¡Sé el primero en enviar uno!")

    # Frase personal
    frase = user.get("frase_personal") if user else None
    if frase:
        st.markdown(f"""
        <div style="background:{TURQ_LIGHT};border-radius:12px;padding:16px;text-align:center;margin-top:16px;border-left:4px solid {TURQ};">
            <div style="font-style:italic;color:{BLACK};font-size:1.05rem;">"{frase}"</div>
            <div style="color:{GRAY};font-size:0.8rem;margin-top:4px;">— Tu frase personal</div>
        </div>""", unsafe_allow_html=True)
