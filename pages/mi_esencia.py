"""Módulo 1: Mi Esencia - Perfil + DISC + Meta Trascendente"""
import streamlit as st
import database as db
from config import DISC_TYPES, TURQ, TURQ_LIGHT, GOLD, BLACK, GRAY
from components.cards import info_card, progress_bar_custom

def render():
    email = st.session_state.current_user
    data = db.get_identidad(email)
    if not data:
        st.error("No se encontró tu perfil.")
        return

    st.markdown("## 👤 Mi Esencia")
    tab1, tab2, tab3 = st.tabs(["📋 Mi Perfil", "🎯 DISC", "✏️ Editar"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{TURQ},#00838F);border-radius:16px;padding:24px;text-align:center;color:white;">
                <div style="font-size:3rem;">👤</div>
                <div style="font-size:1.2rem;font-weight:700;margin-top:8px;">{data['nombre'] or 'Sin nombre'}</div>
                <div style="opacity:0.85;font-size:0.9rem;">{data['puesto'] or 'Sin puesto'}</div>
                <div style="opacity:0.7;font-size:0.8rem;margin-top:4px;">{data['unidad'] or ''} · {data['rol'] or ''}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            disc = data.get("arquetipo_disc")
            if disc and disc in DISC_TYPES:
                d = DISC_TYPES[disc]
                info_card(f"Arquetipo DISC: {d['emoji']} {disc}", d["desc"], color=d["color"])
            meta = data.get("meta_trascendente")
            if meta:
                info_card("🌟 Meta Trascendente", meta, color=GOLD)
                prog = data.get("progreso_meta", 0) or 0
                progress_bar_custom("Progreso hacia tu meta", prog, 100, TURQ)
            frase = data.get("frase_personal")
            if frase:
                st.markdown(f"**💬 Tu Frase:** *\"{frase}\"*")

        if data.get("fortalezas"):
            st.markdown(f"**💪 Fortalezas:** {data['fortalezas']}")
        if data.get("limitantes"):
            st.markdown(f"**🔒 Limitantes identificadas:** {data['limitantes']}")

    with tab2:
        st.markdown("### 🎯 Mi Perfil DISC")
        disc = data.get("arquetipo_disc")
        if disc and disc in DISC_TYPES:
            d = DISC_TYPES[disc]
            st.markdown(f"""
            <div style="background:{d['color']}15;border:2px solid {d['color']};border-radius:16px;padding:24px;text-align:center;">
                <div style="font-size:4rem;">{d['emoji']}</div>
                <div style="font-size:1.5rem;font-weight:700;color:{d['color']};margin:8px 0;">{disc} — {d['name']}</div>
                <div style="color:{BLACK};font-size:1rem;">{d['desc']}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### Puntajes DISC")
            for letter, label in [("disc_d","Dominancia"),("disc_i","Influencia"),("disc_s","Estabilidad"),("disc_c","Conciencia")]:
                val = data.get(letter, 0) or 0
                progress_bar_custom(f"**{label}**", val, 100)

            st.markdown("#### Tips de Comunicación según tu DISC")
            tips = {
                "Rojo": "Sé directo y enfocado en resultados. Evita rodeos. Valora tu tiempo.",
                "Amarillo": "Sé entusiasta y permite espacio para socializar. Valora las ideas creativas.",
                "Verde": "Sé paciente y da tiempo para procesar. No presiones con urgencia.",
                "Azul": "Da datos, detalles y lógica. Respeta la necesidad de precisión."
            }
            for color_name, tip in tips.items():
                is_me = "👈 TÚ" if color_name == disc else ""
                d2 = DISC_TYPES[color_name]
                st.markdown(f"- {d2['emoji']} **{color_name}:** {tip} {is_me}")
        else:
            st.info("Aún no has configurado tu DISC. Ve a la pestaña Editar.")

    with tab3:
        st.markdown("### ✏️ Editar Mi Esencia")
        with st.form("edit_esencia"):
            nombre = st.text_input("Nombre completo", value=data.get("nombre", ""))
            puesto = st.text_input("Puesto", value=data.get("puesto", ""))
            disc_sel = st.selectbox("Arquetipo DISC", ["","Rojo","Amarillo","Verde","Azul"],
                index=["","Rojo","Amarillo","Verde","Azul"].index(data.get("arquetipo_disc","") or ""))

            st.markdown("**Puntajes DISC** (0-100)")
            c1,c2,c3,c4 = st.columns(4)
            dd = c1.number_input("D", 0, 100, data.get("disc_d",0) or 0)
            di = c2.number_input("I", 0, 100, data.get("disc_i",0) or 0)
            ds = c3.number_input("S", 0, 100, data.get("disc_s",0) or 0)
            dc = c4.number_input("C", 0, 100, data.get("disc_c",0) or 0)

            meta = st.text_area("🌟 Meta Trascendente", value=data.get("meta_trascendente","") or "")
            frase = st.text_input("💬 Frase Personal / Mantra", value=data.get("frase_personal","") or "")
            fortalezas = st.text_area("💪 Fortalezas", value=data.get("fortalezas","") or "")
            limitantes = st.text_area("🔒 Limitantes", value=data.get("limitantes","") or "")
            progreso = st.slider("Progreso hacia tu meta (%)", 0, 100, data.get("progreso_meta",0) or 0)

            if st.form_submit_button("💾 Guardar cambios", type="primary"):
                db.update_identidad(email, nombre=nombre, puesto=puesto,
                    arquetipo_disc=disc_sel if disc_sel else None,
                    disc_d=dd, disc_i=di, disc_s=ds, disc_c=dc,
                    meta_trascendente=meta, frase_personal=frase,
                    fortalezas=fortalezas, limitantes=limitantes, progreso_meta=progreso)
                st.success("✅ Perfil actualizado")
                st.rerun()
