"""Módulo 5: Brújula Emocional - IE + Journal + Ejercicios"""
import streamlit as st
import json, os
from datetime import datetime
import database as db
from config import *
from components.cards import radar_chart, progress_bar_custom, metric_card, info_card

def load_ejercicios():
    # Robust path: go from pages/ up to root, then into data/
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "data", "ejercicios.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def render():
    email = st.session_state.current_user
    st.markdown("## 🧠 Mi Brújula Emocional")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📝 Journal", "🎯 Ejercicios", "📋 Evaluar IE", "📈 Evolución"])

    # ── TAB 1: DASHBOARD ──
    with tab1:
        evals = db.get_my_brujula(email)
        if evals:
            last = evals[0]
            cats = [c["nombre"] for c in COMPETENCIAS_IE]
            vals = [last["autoconocimiento"], last["autorregulacion"], last["motivacion"],
                    last["empatia"], last["habilidades_sociales"]]
            st.plotly_chart(radar_chart(cats, vals, f"IE · {last['periodo']}"), use_container_width=True)

            c1, c2, c3 = st.columns(3)
            with c1: metric_card("Promedio IE", f"{last['promedio']}/5")
            with c2: metric_card("⬆️ Fortaleza", last["comp_alta"], color=GREEN)
            with c3: metric_card("⬇️ Oportunidad", last["comp_baja"], color=RED)

            st.markdown("#### Detalle por Competencia")
            for comp, val in zip(COMPETENCIAS_IE, vals):
                progress_bar_custom(f"{comp['emoji']} {comp['nombre']}", val, 5, comp["color"])

            c1, c2 = st.columns(2)
            with c1: metric_card("📝 Journal este mes", last.get("journal_mes", 0))
            with c2: metric_card("🎯 Ejercicios este mes", last.get("ejercicios_mes", 0))
        else:
            info_card("Sin evaluación IE", "Completa tu primera autoevaluación en la pestaña 'Evaluar IE'.", "🧠")

        # Sugerencia personalizada
        checkins = db.get_my_checkins(email, 4)
        if checkins:
            avg_estres = sum(c["nivel_estres"] for c in checkins) / len(checkins)
            if avg_estres >= 3.5:
                st.warning("🎯 **Sugerencia:** Tu estrés promedio es alto. Te recomendamos los ejercicios de respiración 4-7-8 o Box Breathing.")
            elif avg_estres <= 2:
                st.success("🌟 **¡Bien hecho!** Tu nivel de estrés es bajo. Mantén el ritmo.")

    # ── TAB 2: JOURNAL ──
    with tab2:
        st.markdown("### 📝 Mi Diario Emocional")
        with st.form("journal_form"):
            emociones = st.multiselect("¿Qué emociones sientes ahora?", ALL_ETIQUETAS)
            intensidad = st.slider("Intensidad (1-10)", 1, 10, 5)
            trigger = st.text_area("¿Qué situación disparó esta emoción?", placeholder="Ej: Una conversación difícil...")
            pensamiento = st.text_area("¿Qué pensamiento acompaña esta emoción?", placeholder="Ej: Siento que no soy suficiente...")
            reflexion = st.text_area("¿Qué aprendizaje te deja este momento?", placeholder="Ej: Necesito pedir ayuda...")
            contexto = st.radio("Contexto", ["Trabajo", "Personal", "Social", "Salud"], horizontal=True)

            with st.expander("🎯 ¿Usaste alguna estrategia? (opcional)"):
                estrategia = st.text_input("¿Qué hiciste para manejar la emoción?")
                efectividad = st.slider("¿Qué tan efectiva fue? (1-5)", 1, 5, 3)

            if st.form_submit_button("📝 Guardar en Journal", type="primary"):
                if not emociones:
                    st.error("Selecciona al menos una emoción.")
                else:
                    ok, msg = db.save_journal(email, emociones, intensidad, trigger,
                        pensamiento, reflexion, estrategia if estrategia else None,
                        efectividad if estrategia else None, contexto)
                    if ok: st.success(f"✅ {msg}")
                    st.rerun()

        st.divider()
        st.markdown("#### 📖 Mis Entradas Recientes")
        entries = db.get_my_journal(email, 10)
        for e in entries:
            fecha = e["fecha"][:10] if e.get("fecha") else ""
            emociones = e.get("emociones", "")
            st.markdown(f"""
            <div style="background:white;border-radius:12px;padding:14px;border-left:4px solid #7E57C2;
            box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;">
                    <span style="font-weight:600;">{emociones}</span>
                    <span style="color:{GRAY};font-size:0.8rem;">{fecha} · {e.get('dia_semana','')} {e.get('hora_dia','')}</span>
                </div>
                <div style="color:{GRAY};font-size:0.85rem;">Intensidad: {e.get('intensidad','')}/10 · {e.get('contexto','')}</div>
                {f'<div style="margin-top:6px;font-style:italic;color:{BLACK};">"{e["reflexion"]}"</div>' if e.get("reflexion") else ''}
            </div>""", unsafe_allow_html=True)

    # ── TAB 3: EJERCICIOS ──
    with tab3:
        st.markdown("### 🎯 Catálogo de Ejercicios")
        ejercicios = load_ejercicios()
        comp_filter = st.selectbox("Filtrar por competencia",
            ["Todas"] + [c["nombre"] for c in COMPETENCIAS_IE])
        
        filtered = ejercicios if comp_filter == "Todas" else [e for e in ejercicios if e["competencia"] == comp_filter]
        
        for ej in filtered:
            with st.expander(f"{'🟢' if ej['dificultad']=='Principiante' else '🟡' if ej['dificultad']=='Intermedio' else '🔴'} {ej['nombre']} · {ej['duracion']} min · {ej['competencia']}"):
                st.markdown(f"**{ej['descripcion']}**")
                st.markdown(f"📋 **Instrucciones:**\n\n{ej['instrucciones']}")
                st.markdown(f"✅ **Beneficio:** {ej['beneficio']}")
                st.markdown(f"⏰ **Mejor momento:** {ej['momento']}")
                
                if st.button(f"✅ Completar ejercicio", key=f"ej_{ej['id']}"):
                    with db.get_db() as conn:
                        lid = f"LOG_{email.split('@')[0]}_{int(datetime.now().timestamp())}"
                        conn.execute("INSERT INTO ejercicios_log VALUES (?,?,?,?,?,?,?,?,?,?)",
                            (lid, email, ej["id"], datetime.now().isoformat(), ej["duracion"],
                             0, "", "", "", ej["competencia"]))
                    st.success(f"✅ ¡Ejercicio '{ej['nombre']}' completado!")
                    st.rerun()

    # ── TAB 4: EVALUACIÓN IE ──
    with tab4:
        st.markdown("### 📋 Autoevaluación de Inteligencia Emocional")
        st.caption("Evalúa cada competencia del 1 al 5 con honestidad. Esta evaluación es mensual.")
        with st.form("brujula_eval"):
            puntajes = {}
            for comp in COMPETENCIAS_IE:
                st.markdown(f"**{comp['emoji']} {comp['nombre']}**")
                st.caption(comp["pregunta"])
                val = st.slider("", 1, 5, 3, key=f"ie_{comp['nombre']}", label_visibility="collapsed")
                desc = ESCALA.get(val, "")
                st.caption(f"Nivel: {desc}")
                puntajes[comp["nombre"]] = val
            reflexion = st.text_area("💭 Reflexión general", placeholder="¿Qué descubriste de tu IE este mes?")
            if st.form_submit_button("🧠 Guardar Evaluación IE", type="primary"):
                ok, msg = db.save_brujula(email,
                    {"autoconocimiento": puntajes["Autoconocimiento"],
                     "autorregulacion": puntajes["Autorregulación"],
                     "motivacion": puntajes["Motivación"],
                     "empatia": puntajes["Empatía"],
                     "habilidades_sociales": puntajes["Habilidades Sociales"]}, reflexion)
                if ok: st.success(f"✅ {msg}")
                else: st.warning(msg)
                st.rerun()

    # ── TAB 5: EVOLUCIÓN ──
    with tab5:
        st.markdown("### 📈 Mi Evolución en IE")
        evals = db.get_my_brujula(email)
        if len(evals) >= 2:
            import plotly.graph_objects as go
            periodos = [e["periodo"] for e in reversed(evals)]
            fig = go.Figure()
            for comp, key in zip(COMPETENCIAS_IE, ["autoconocimiento","autorregulacion","motivacion","empatia","habilidades_sociales"]):
                vals = [e[key] for e in reversed(evals)]
                fig.add_trace(go.Scatter(x=periodos, y=vals, name=comp["nombre"],
                    mode="lines+markers", line=dict(color=comp["color"], width=2)))
            fig.update_layout(height=400, yaxis=dict(range=[0,5.5]), legend=dict(orientation="h"))
            st.plotly_chart(fig, use_container_width=True)
        elif evals:
            st.info("Necesitas al menos 2 evaluaciones para ver la evolución. ¡Sigue así!")
        else:
            st.info("Completa tu primera evaluación IE para empezar a ver tu evolución.")
