"""Módulo 2: Mi Estrategia - OKR + Metas"""
import streamlit as st
from datetime import datetime
import database as db
from config import TURQ, GREEN, YELLOW, RED, GRAY
from components.cards import metric_card, progress_bar_custom

def render():
    email = st.session_state.current_user
    st.markdown("## 🎯 Mi Estrategia")
    tab1, tab2 = st.tabs(["📋 Mis Metas", "➕ Nueva Meta"])

    with tab1:
        with db.get_db() as conn:
            metas = db.dict_rows(conn.execute(
                "SELECT * FROM metas WHERE email=? ORDER BY fecha_creacion DESC", (email,)).fetchall())
        if metas:
            for m in metas:
                prog = m["progreso"] or 0
                color = GREEN if prog >= 75 else YELLOW if prog >= 40 else RED
                estado_emoji = {"Pendiente":"⏳","En Progreso":"🔄","Completado":"✅","Cancelado":"❌"}.get(m["estado"],"⏳")
                st.markdown(f"""
                <div style="background:white;border-radius:12px;padding:16px;border-left:4px solid {color};
                box-shadow:0 2px 6px rgba(0,0,0,0.06);margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;">
                        <span style="font-weight:600;">{estado_emoji} {m['objetivo']}</span>
                        <span style="color:{GRAY};font-size:0.8rem;">{m['periodo']}</span>
                    </div>
                    <div style="color:{GRAY};font-size:0.85rem;margin:4px 0;">{m['tipo']}</div>
                </div>""", unsafe_allow_html=True)
                progress_bar_custom("Progreso", prog, 100, color)
                if m.get("kr1"):
                    st.caption(f"KR1: {m['kr1']}")
                if m.get("kr2"):
                    st.caption(f"KR2: {m['kr2']}")
                if m.get("kr3"):
                    st.caption(f"KR3: {m['kr3']}")
                
                c1, c2, c3 = st.columns(3)
                new_prog = c1.number_input("Actualizar %", 0, 100, prog, key=f"prog_{m['meta_id']}")
                new_estado = c2.selectbox("Estado", ["Pendiente","En Progreso","Completado","Cancelado"],
                    index=["Pendiente","En Progreso","Completado","Cancelado"].index(m["estado"]),
                    key=f"est_{m['meta_id']}")
                if c3.button("💾", key=f"save_{m['meta_id']}"):
                    with db.get_db() as conn:
                        conn.execute("UPDATE metas SET progreso=?, estado=? WHERE meta_id=?",
                            (new_prog, new_estado, m["meta_id"]))
                    st.success("Actualizado")
                    st.rerun()
                st.divider()
        else:
            st.info("No tienes metas registradas. ¡Crea tu primera meta!")

    with tab2:
        st.markdown("### ➕ Nueva Meta / OKR")
        with st.form("new_meta"):
            tipo = st.selectbox("Tipo", ["OKR", "Meta Personal", "Meta Equipo"])
            periodo = st.selectbox("Periodo", ["2026-Q1","2026-Q2","2026-Q3","2026-Q4","2026-Anual"])
            objetivo = st.text_area("🎯 Objetivo", placeholder="¿Qué quieres lograr?")
            kr1 = st.text_input("KR1 - Resultado Clave 1", placeholder="¿Cómo sabrás que lo lograste?")
            kr2 = st.text_input("KR2 - Resultado Clave 2 (opcional)")
            kr3 = st.text_input("KR3 - Resultado Clave 3 (opcional)")
            fecha_limite = st.date_input("Fecha límite")

            if st.form_submit_button("✅ Crear Meta", type="primary"):
                if not objetivo:
                    st.error("El objetivo es obligatorio.")
                else:
                    mid = f"{email}_{periodo}_{int(datetime.now().timestamp())}"
                    with db.get_db() as conn:
                        conn.execute("INSERT INTO metas VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                            (mid, email, tipo, periodo, objetivo, kr1, kr2, kr3,
                             0, "Pendiente", datetime.now().isoformat(), fecha_limite.isoformat()))
                    st.success("🎯 Meta creada exitosamente!")
                    st.rerun()
