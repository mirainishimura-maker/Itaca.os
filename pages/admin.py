"""Dashboard Admin - Analytics para Mirai"""
import streamlit as st
import database as db
from config import TURQ, GREEN, RED, YELLOW, GOLD, GRAY
from components.cards import metric_card
import plotly.graph_objects as go

def render():
    if st.session_state.get("user_rol") != "Admin":
        st.error("🔒 Acceso restringido. Solo Admin puede ver esta pantalla.")
        return
    
    st.markdown("## 📊 Dashboard Admin — Mirai")
    analytics = db.get_analytics()

    # Métricas principales
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("👥 Activos", analytics["total_users"], color=TURQ)
    with c2: metric_card("💙 Check-ins", analytics["checkins_week"], f"Tasa: {analytics['tasa_checkin']}%", GREEN)
    with c3: metric_card("😰 Estrés Prom.", f"{analytics['avg_estres']}/5",
        color=GREEN if analytics["avg_estres"] < 3 else YELLOW if analytics["avg_estres"] < 4 else RED)
    with c4: metric_card("🔦 Faros (mes)", analytics["faros_mes"], f"Total: {analytics['total_faros']}", GOLD)

    st.divider()

    # Alertas
    if analytics["alertas"] > 0:
        st.error(f"🚨 **{analytics['alertas']} alertas de bienestar** esta semana (estrés ≥ 4). Revisa los check-ins.")
    
    # Check-ins detallados
    st.markdown("### 💙 Check-ins Recientes (toda la organización)")
    with db.get_db() as conn:
        all_ci = db.dict_rows(conn.execute("""
            SELECT c.*, i.nombre FROM checkins c
            JOIN identidad i ON c.email = i.email
            ORDER BY c.fecha DESC LIMIT 20""").fetchall())
    
    if all_ci:
        import pandas as pd
        df = pd.DataFrame(all_ci)
        cols_show = ["nombre","estado_general","nivel_estres","area_preocupacion","fecha"]
        if all(c in df.columns for c in cols_show):
            st.dataframe(df[cols_show].rename(columns={
                "nombre":"Nombre","estado_general":"Estado","nivel_estres":"Estrés",
                "area_preocupacion":"Área","fecha":"Fecha"}), use_container_width=True)

    # Faros por tipo
    st.markdown("### 🔦 Distribución de Faros")
    with db.get_db() as conn:
        faros_by_type = db.dict_rows(conn.execute(
            "SELECT tipo_faro, COUNT(*) as total FROM faros GROUP BY tipo_faro").fetchall())
    if faros_by_type:
        fig = go.Figure(data=[go.Pie(
            labels=[f["tipo_faro"] for f in faros_by_type],
            values=[f["total"] for f in faros_by_type],
            marker_colors=[TURQ, GOLD, GREEN], hole=0.4)])
        fig.update_layout(height=300, margin=dict(l=20,r=20,t=20,b=20))
        st.plotly_chart(fig, use_container_width=True)

    # Estrés por equipo
    st.markdown("### 😰 Estrés Promedio por Unidad")
    with db.get_db() as conn:
        by_unit = db.dict_rows(conn.execute("""
            SELECT i.unidad, AVG(c.nivel_estres) as avg_estres, COUNT(DISTINCT c.email) as personas
            FROM checkins c JOIN identidad i ON c.email = i.email
            WHERE c.fecha > datetime('now', '-30 days')
            GROUP BY i.unidad""").fetchall())
    if by_unit:
        fig = go.Figure(data=[go.Bar(
            x=[u["unidad"] for u in by_unit],
            y=[round(u["avg_estres"],1) for u in by_unit],
            marker_color=[GREEN if u["avg_estres"]<3 else YELLOW if u["avg_estres"]<4 else RED for u in by_unit])])
        fig.update_layout(height=300, yaxis=dict(range=[0,5.5]), yaxis_title="Estrés Promedio")
        st.plotly_chart(fig, use_container_width=True)
