"""Reusable UI components - cards, metrics, charts"""
import streamlit as st
import plotly.graph_objects as go
from config import TURQ, TURQ_DARK, TURQ_LIGHT, GREEN, RED, YELLOW, GOLD, WHITE, BLACK, GRAY

def metric_card(label, value, delta=None, color=TURQ):
    dc = f"color: {GREEN}" if delta and "+" in str(delta) else f"color: {RED}" if delta and "-" in str(delta) else ""
    st.markdown(f"""
    <div style="background:white;border-radius:16px;padding:20px;border-left:4px solid {color};
    box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:12px;">
        <div style="color:{GRAY};font-size:0.85rem;font-weight:500;">{label}</div>
        <div style="font-size:2rem;font-weight:700;color:{BLACK};margin:4px 0;">{value}</div>
        {f'<div style="{dc};font-size:0.8rem;">{delta}</div>' if delta else ''}
    </div>""", unsafe_allow_html=True)

def info_card(title, content, icon="", color=TURQ):
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, {color}15, {color}08);border-radius:16px;
    padding:20px;border:1px solid {color}30;margin-bottom:12px;">
        <div style="font-size:1.1rem;font-weight:600;color:{color};margin-bottom:8px;">{icon} {title}</div>
        <div style="color:{BLACK};font-size:0.95rem;line-height:1.6;">{content}</div>
    </div>""", unsafe_allow_html=True)

def faro_card(faro):
    from config import TIPOS_FARO
    info = TIPOS_FARO.get(faro["tipo_faro"], {})
    emoji = info.get("emoji", "🔦")
    color = info.get("color", TURQ)
    fecha = faro["fecha_envio"][:10] if faro.get("fecha_envio") else ""
    st.markdown(f"""
    <div style="background:white;border-radius:16px;padding:16px;border-left:4px solid {color};
    box-shadow:0 2px 8px rgba(0,0,0,0.06);margin-bottom:12px;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-weight:600;color:{BLACK};">{emoji} {faro['nombre_emisor']} → {faro['nombre_receptor']}</span>
            <span style="color:{GRAY};font-size:0.8rem;">{fecha}</span>
        </div>
        <div style="color:{color};font-size:0.85rem;font-weight:500;margin:4px 0;">{faro['tipo_faro']} · {faro.get('animal','')}</div>
        <div style="color:{BLACK};font-size:0.9rem;margin-top:8px;font-style:italic;">"{faro['mensaje']}"</div>
        <div style="color:{GRAY};font-size:0.8rem;margin-top:6px;">👏 {faro.get('celebraciones',0)} celebraciones</div>
    </div>""", unsafe_allow_html=True)

def checkin_card(ci):
    from config import ESTADOS_CHECKIN
    emoji = ESTADOS_CHECKIN.get(ci["estado_general"], "😐")
    estres = ci["nivel_estres"]
    sc = GREEN if estres <= 2 else YELLOW if estres <= 3 else RED
    fecha = ci["fecha"][:10] if ci.get("fecha") else ""
    nombre = ci.get("nombre", "")
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:14px;border-left:4px solid {sc};
    box-shadow:0 1px 4px rgba(0,0,0,0.05);margin-bottom:8px;">
        <div style="display:flex;justify-content:space-between;">
            <span style="font-weight:600;">{emoji} {ci['estado_general']} {f'· {nombre}' if nombre else ''}</span>
            <span style="color:{GRAY};font-size:0.8rem;">{fecha}</span>
        </div>
        <div style="color:{sc};font-size:0.85rem;">Estrés: {'🟢' * min(estres,5)}{'⚪' * (5-min(estres,5))} {estres}/5</div>
    </div>""", unsafe_allow_html=True)

def progress_bar_custom(label, value, max_val=5, color=TURQ):
    pct = min((value / max_val) * 100, 100)
    sc = GREEN if value >= 4 else YELLOW if value >= 2.5 else RED
    st.markdown(f"""
    <div style="margin-bottom:10px;">
        <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="font-size:0.9rem;font-weight:500;">{label}</span>
            <span style="font-weight:700;color:{sc};">{value}/{max_val}</span>
        </div>
        <div style="background:#E0E0E0;border-radius:8px;height:10px;overflow:hidden;">
            <div style="background:{sc};width:{pct}%;height:100%;border-radius:8px;transition:width 0.5s;"></div>
        </div>
    </div>""", unsafe_allow_html=True)

def radar_chart(categories, values, title="", max_val=5):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]],
        fill='toself', fillcolor=f'rgba(38,198,218,0.2)', line=dict(color=TURQ, width=2),
        marker=dict(size=8, color=TURQ)))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max_val], tickfont=dict(size=10)),
                   angularaxis=dict(tickfont=dict(size=12, family="Inter"))),
        showlegend=False, title=dict(text=title, font=dict(size=16, family="Inter")),
        margin=dict(l=60, r=60, t=60, b=40), height=380,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def semaforo(valor, umbrales=(2.5, 4)):
    if valor >= umbrales[1]: return "🟢", GREEN, "Excelente"
    elif valor >= umbrales[0]: return "🟡", YELLOW, "En desarrollo"
    else: return "🔴", RED, "Necesita atención"
