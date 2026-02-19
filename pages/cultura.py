"""Módulo 4: Cultura Ítaca - Check-ins + Faros + Pilares I+M"""
import streamlit as st
from datetime import datetime
import database as db
from config import *
from components.cards import faro_card, checkin_card, info_card, metric_card

def render():
    email = st.session_state.current_user
    st.markdown("## ❤️ Cultura Ítaca")
    
    default_tab = 0
    if st.session_state.get("cultura_tab") == "Check-in": default_tab = 0
    elif st.session_state.get("cultura_tab") == "Faros": default_tab = 1
    st.session_state.pop("cultura_tab", None)

    tab1, tab2, tab3, tab4 = st.tabs(["💙 Check-in", "🔦 Faros", "❤️ Cultura I+M", "🌍 Muro Público"])

    # ── TAB 1: CHECK-IN ──
    with tab1:
        done = db.checkin_done_this_week(email)
        if not done:
            st.markdown("### 💙 ¿Cómo te sientes esta semana?")
            with st.form("checkin_form"):
                st.markdown("**¿Cómo te sientes hoy?**")
                estado = st.radio("", list(ESTADOS_CHECKIN.keys()),
                    format_func=lambda x: f"{ESTADOS_CHECKIN[x]} {x}", horizontal=True,
                    label_visibility="collapsed")
                st.markdown("**Nivel de estrés esta semana**")
                estres = st.slider("1 = Tranquilo → 5 = Muy estresado", 1, 5, 3, label_visibility="collapsed")
                cols_stress = st.columns(5)
                for i in range(5):
                    with cols_stress[i]:
                        labels = ["😌 Tranquilo","😊 Leve","😐 Moderado","😰 Alto","🤯 Muy alto"]
                        st.caption(labels[i])
                
                area = st.radio("**¿En qué área está tu preocupación principal?**",
                    AREAS_PREOCUPACION, horizontal=True)
                etiquetas = st.multiselect("**Selecciona las emociones que te describen hoy**", ALL_ETIQUETAS)
                comentario = st.text_area("Si quieres compartir algo más (confidencial, solo RH lo ve)",
                    placeholder="Este espacio es tuyo...", help="Solo Mirai puede ver este comentario.")
                
                if st.form_submit_button("💙 Registrar Check-in", type="primary"):
                    ok, msg = db.save_checkin(email, estado, estres, area, etiquetas, comentario)
                    if ok:
                        st.success(f"✅ {msg}")
                        st.balloons()
                    else:
                        st.warning(msg)
                    st.rerun()
        else:
            st.success("✅ Ya hiciste tu check-in esta semana. ¡Gracias por compartir!")

        st.markdown("#### 📊 Mi Historial")
        checkins = db.get_my_checkins(email, 10)
        if checkins:
            for ci in checkins:
                checkin_card(ci)
        else:
            st.info("Aún no tienes check-ins registrados.")

    # ── TAB 2: FAROS ──
    with tab2:
        st.markdown("### 🔦 Enviar un Faro de Reconocimiento")
        users = db.get_all_users()
        otros = [u for u in users if u["email"] != email]
        
        with st.form("faro_form"):
            receptor = st.selectbox("¿A quién quieres reconocer?",
                [u["email"] for u in otros],
                format_func=lambda e: next((u["nombre"] for u in otros if u["email"]==e), e))
            
            st.markdown("**¿Qué tipo de Faro quieres encender?**")
            tipo_opts = list(TIPOS_FARO.keys())
            tipo = st.radio("", tipo_opts,
                format_func=lambda t: f"{TIPOS_FARO[t]['emoji']} {t} — {TIPOS_FARO[t]['desc']}",
                label_visibility="collapsed")
            
            info = TIPOS_FARO[tipo]
            st.markdown(f"*Pilar: **{info['pilar']}** · Gung Ho: **{info['animal']}***")
            
            mensaje = st.text_area("✍️ Escribe tu mensaje de reconocimiento",
                placeholder="Ej: Gracias por ayudarme con el proyecto...", min_value=None)
            
            if st.form_submit_button("🔦 Encender Faro", type="primary"):
                if not mensaje or len(mensaje) < 10:
                    st.error("El mensaje debe tener al menos 10 caracteres.")
                else:
                    ok, msg = db.save_faro(email, receptor, tipo, mensaje)
                    if ok:
                        st.success(f"✅ {msg}")
                        st.balloons()
                    st.rerun()

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📥 Faros Recibidos")
            recibidos = db.get_faros_recibidos(email, 5)
            if recibidos:
                for f in recibidos: faro_card(f)
            else: st.caption("Aún no has recibido faros.")
        with col2:
            st.markdown("#### 📤 Faros Enviados")
            enviados = db.get_faros_enviados(email, 5)
            if enviados:
                for f in enviados: faro_card(f)
            else: st.caption("Aún no has enviado faros.")

    # ── TAB 3: CULTURA I+M ──
    with tab3:
        st.markdown("### ❤️ Los Pilares I+M de Ítaca")
        st.caption("Nuestra cultura se vive a través de 3 pilares conectados con la filosofía Gung Ho.")
        
        for pilar in PILARES:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, {pilar['color']}12, {pilar['color']}05);
            border-radius:16px;padding:24px;border:2px solid {pilar['color']}40;margin-bottom:20px;">
                <div style="font-size:1.3rem;font-weight:700;color:{pilar['color']};">{pilar['animal']} {pilar['nombre']}</div>
                <div style="color:{GRAY};font-size:0.85rem;margin:4px 0;">Gung Ho: {pilar['gungho']} · Faro: {pilar['faro']}</div>
                <div style="color:{BLACK};font-size:0.95rem;margin:12px 0;line-height:1.6;">{pilar['desc']}</div>
                <div style="color:{pilar['color']};font-style:italic;font-weight:600;">"{pilar['frase']}"</div>
                <div style="background:{pilar['color']}15;border-radius:8px;padding:10px;margin-top:12px;">
                    <strong>Principio Gung Ho:</strong> {pilar['principio']}
                </div>
            </div>""", unsafe_allow_html=True)

    # ── TAB 4: MURO PÚBLICO ──
    with tab4:
        st.markdown("### 🌍 Muro Público de Faros")
        faros = db.get_faros_publicos(20)
        if faros:
            c1, c2, c3 = st.columns(3)
            total_valor = sum(1 for f in faros if f["tipo_faro"]=="Faro de Valor")
            total_guia = sum(1 for f in faros if f["tipo_faro"]=="Faro de Guía")
            total_aliento = sum(1 for f in faros if f["tipo_faro"]=="Faro de Aliento")
            with c1: metric_card("🐿️ Valor", total_valor, color=TURQ)
            with c2: metric_card("🦫 Guía", total_guia, color=GOLD)
            with c3: metric_card("🪿 Aliento", total_aliento, color=GREEN)
            
            for f in faros:
                faro_card(f)
                if st.button(f"👏 Celebrar", key=f"cel_{f['faro_id']}"):
                    db.celebrar_faro(f["faro_id"])
                    st.rerun()
        else:
            st.info("Aún no hay faros públicos.")
