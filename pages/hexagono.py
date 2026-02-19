"""Módulo 3: Hexágono de Liderazgo"""
import streamlit as st
import database as db
from config import DIMENSIONES_HEXAGONO, TURQ, GREEN, YELLOW, RED, GRAY
from components.cards import radar_chart, progress_bar_custom, metric_card, checkin_card, info_card

def render():
    email = st.session_state.current_user
    st.markdown("## 🧭 Mi Hexágono de Liderazgo")
    tab1, tab2, tab3 = st.tabs(["📊 Mi Hexágono", "✏️ Evaluarme", "⛵ Mi Tripulación"])

    with tab1:
        evals = db.get_my_hexagono(email)
        if evals:
            last = evals[0]
            cats = [d["nombre"] for d in DIMENSIONES_HEXAGONO]
            vals = [last["vision"], last["planificacion"], last["encaje"],
                    last["entrenamiento"], last["evaluacion_mejora"], last["reconocimiento"]]
            st.plotly_chart(radar_chart(cats, vals, f"Hexágono · {last['periodo']}"), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1: metric_card("Promedio", f"{last['promedio']}/5")
            with col2: metric_card("⬆️ Fortaleza", last["dim_alta"], color=GREEN)
            with col3: metric_card("⬇️ Oportunidad", last["dim_baja"], color=RED)
            
            st.markdown("#### Detalle por Dimensión")
            for d, v in zip(DIMENSIONES_HEXAGONO, vals):
                progress_bar_custom(f"{d['emoji']} {d['nombre']}", v, 5)

            if len(evals) > 1:
                st.markdown("#### 📈 Evolución")
                import plotly.graph_objects as go
                periodos = [e["periodo"] for e in reversed(evals)]
                promedios = [e["promedio"] for e in reversed(evals)]
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=periodos, y=promedios, mode="lines+markers",
                    line=dict(color=TURQ, width=3), marker=dict(size=10)))
                fig.update_layout(height=250, margin=dict(l=40,r=20,t=20,b=40),
                    yaxis=dict(range=[0,5.5]), xaxis_title="Periodo", yaxis_title="Promedio")
                st.plotly_chart(fig, use_container_width=True)
        else:
            info_card("Sin evaluación aún", "Completa tu primera autoevaluación del Hexágono en la pestaña 'Evaluarme'.", "🧭")

    with tab2:
        st.markdown("### ✏️ Autoevaluación Mensual")
        st.caption("Evalúa cada dimensión del 1 al 5 con honestidad.")
        with st.form("hex_eval"):
            puntajes = {}
            for d in DIMENSIONES_HEXAGONO:
                st.markdown(f"**{d['emoji']} {d['nombre']}**")
                st.caption(d["pregunta"])
                puntajes[d["nombre"]] = st.slider("", 1, 5, 3, key=f"hex_{d['nombre']}", label_visibility="collapsed")
            reflexion = st.text_area("💭 Reflexión", placeholder="¿Qué aprendiste de tu liderazgo este mes?")
            if st.form_submit_button("📊 Guardar Evaluación", type="primary"):
                ok, msg = db.save_hexagono(email,
                    {"vision": puntajes["Visión Corporativa"], "planificacion": puntajes["Planificación"],
                     "encaje": puntajes["Encaje de Talento"], "entrenamiento": puntajes["Entrenamiento"],
                     "evaluacion_mejora": puntajes["Evaluación y Mejora"], "reconocimiento": puntajes["Reconocimiento"]},
                    reflexion)
                if ok: st.success(f"✅ {msg}")
                else: st.warning(msg)
                st.rerun()

    with tab3:
        st.markdown("### ⛵ Mi Tripulación")
        team = db.get_team_members(email)
        if team:
            for m in team:
                disc = m.get("arquetipo_disc", "")
                from config import DISC_TYPES
                d = DISC_TYPES.get(disc, {})
                emoji = d.get("emoji", "👤")
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:14px;border-left:4px solid {TURQ};
                box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:8px;">
                    <div style="font-weight:600;">{emoji} {m['nombre']}</div>
                    <div style="color:{GRAY};font-size:0.85rem;">{m.get('puesto','')}</div>
                </div>""", unsafe_allow_html=True)
            
            st.markdown("#### 📊 Check-ins del Equipo")
            team_ci = db.get_team_checkins(email)
            for ci in team_ci[:10]:
                checkin_card(ci)
        else:
            st.info("No tienes miembros de equipo asignados.")
