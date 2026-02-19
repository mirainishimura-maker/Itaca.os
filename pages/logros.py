"""Logros y Gamificación"""
import streamlit as st
import database as db
from config import TURQ, GOLD, GREEN, GRAY, BLACK
from components.cards import metric_card

def render():
    email = st.session_state.current_user
    st.markdown("## 🏆 Mis Logros")
    
    puntos = db.get_total_puntos(email)
    logros = db.get_my_logros(email)
    
    c1, c2, c3 = st.columns(3)
    with c1: metric_card("⭐ Puntos Totales", puntos, color=GOLD)
    with c2: metric_card("🏆 Badges", len(logros), color=GREEN)
    with c3:
        nivel = "🥉 Marinero" if puntos < 50 else "🥈 Navegante" if puntos < 150 else "🥇 Capitán" if puntos < 300 else "👑 Almirante"
        metric_card("🎖️ Nivel", nivel, color=TURQ)

    st.divider()
    
    if logros:
        st.markdown("### 🏆 Badges Obtenidos")
        cols = st.columns(3)
        for i, l in enumerate(logros):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:white;border-radius:16px;padding:20px;text-align:center;
                border:2px solid {GOLD}40;box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:12px;">
                    <div style="font-size:2.5rem;">{l.get('icono','🏆')}</div>
                    <div style="font-weight:700;color:{BLACK};margin:8px 0;">{l['nombre_badge']}</div>
                    <div style="color:{GRAY};font-size:0.85rem;">{l['descripcion']}</div>
                    <div style="color:{GOLD};font-weight:600;margin-top:6px;">+{l['puntos']} pts</div>
                    <div style="color:{GRAY};font-size:0.75rem;">{l['fecha'][:10]}</div>
                </div>""", unsafe_allow_html=True)
    else:
        st.info("Aún no tienes badges. ¡Haz tu primer check-in o envía un faro para desbloquear tu primer logro!")

    # Badges disponibles
    st.markdown("### 🔒 Badges por Desbloquear")
    all_badges = [
        ("🔦","Primer Faro","Envía tu primer faro",10,"Cultura"),
        ("🔦","Iluminador","5 faros en un mes",25,"Cultura"),
        ("💙","Bienestar Constante","4 check-ins consecutivos",15,"Cultura"),
        ("📝","Primer Journal","1 entrada de journal",10,"IE"),
        ("📝","Escritor Emocional","10 entradas de journal",25,"IE"),
        ("🎯","Primera Respiración","1 ejercicio completado",10,"IE"),
        ("🧠","Brújula Calibrada","Primera autoevaluación IE",15,"IE"),
        ("🧭","Hexágono Activo","Primera evaluación de liderazgo",15,"Liderazgo"),
        ("⭐","Estrella Reconocida","5 faros recibidos en un mes",30,"Cultura"),
    ]
    obtained_ids = [l["nombre_badge"] for l in logros]
    locked = [b for b in all_badges if b[1] not in obtained_ids]
    if locked:
        cols = st.columns(3)
        for i, b in enumerate(locked):
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background:#F5F5F5;border-radius:16px;padding:20px;text-align:center;
                opacity:0.5;margin-bottom:12px;">
                    <div style="font-size:2.5rem;">🔒</div>
                    <div style="font-weight:600;color:{GRAY};">{b[1]}</div>
                    <div style="color:{GRAY};font-size:0.8rem;">{b[2]}</div>
                    <div style="color:{GRAY};font-size:0.75rem;">+{b[3]} pts</div>
                </div>""", unsafe_allow_html=True)
