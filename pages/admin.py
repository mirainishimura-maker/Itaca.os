"""Dashboard Admin - Analytics + Gestión de Colaboradores para Mirai"""
import streamlit as st
import database as db
from config import TURQ, GREEN, RED, YELLOW, GOLD, GRAY, ROLES
from components.cards import metric_card
import plotly.graph_objects as go


def render():
    if st.session_state.get("user_rol") != "Admin":
        st.error("🔒 Acceso restringido. Solo Admin puede ver esta pantalla.")
        return

    st.markdown("## 📊 Panel de Administración")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Analytics", "👥 Gestionar Colaboradores", "➕ Agregar Nuevo", "🔧 Herramientas"
    ])

    # ══════════════════════════════════════
    # TAB 1: ANALYTICS
    # ══════════════════════════════════════
    with tab1:
        analytics = db.get_analytics()
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("👥 Activos", analytics["total_users"], color=TURQ)
        with c2:
            metric_card("💙 Check-ins", analytics["checkins_week"],
                        f"Tasa: {analytics['tasa_checkin']}%", GREEN)
        with c3:
            metric_card("😰 Estrés Prom.", f"{analytics['avg_estres']}/5",
                        color=GREEN if analytics["avg_estres"] < 3
                        else YELLOW if analytics["avg_estres"] < 4 else RED)
        with c4:
            metric_card("🔦 Faros (mes)", analytics["faros_mes"],
                        f"Total: {analytics['total_faros']}", GOLD)

        st.divider()

        if analytics["alertas"] > 0:
            st.error(f"🚨 **{analytics['alertas']} alertas de bienestar** "
                     f"esta semana (estrés ≥ 4).")

        st.markdown("### 💙 Check-ins Recientes")
        with db.get_db() as conn:
            all_ci = db.dict_rows(conn.execute("""
                SELECT c.*, i.nombre FROM checkins c
                JOIN identidad i ON c.email = i.email
                ORDER BY c.fecha DESC LIMIT 20""").fetchall())
        if all_ci:
            import pandas as pd
            df = pd.DataFrame(all_ci)
            cols_show = ["nombre", "estado_general", "nivel_estres",
                         "area_preocupacion", "fecha"]
            if all(c in df.columns for c in cols_show):
                st.dataframe(df[cols_show].rename(columns={
                    "nombre": "Nombre", "estado_general": "Estado",
                    "nivel_estres": "Estrés", "area_preocupacion": "Área",
                    "fecha": "Fecha"}), use_container_width=True)

        st.markdown("### 🔦 Distribución de Faros")
        with db.get_db() as conn:
            faros_by_type = db.dict_rows(conn.execute(
                "SELECT tipo_faro, COUNT(*) as total FROM faros "
                "GROUP BY tipo_faro").fetchall())
        if faros_by_type:
            fig = go.Figure(data=[go.Pie(
                labels=[f["tipo_faro"] for f in faros_by_type],
                values=[f["total"] for f in faros_by_type],
                marker_colors=[TURQ, GOLD, GREEN], hole=0.4)])
            fig.update_layout(height=300, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 😰 Estrés Promedio por Unidad")
        with db.get_db() as conn:
            by_unit = db.dict_rows(conn.execute("""
                SELECT i.unidad, AVG(c.nivel_estres) as avg_estres,
                       COUNT(DISTINCT c.email) as personas
                FROM checkins c JOIN identidad i ON c.email = i.email
                WHERE c.fecha > datetime('now', '-30 days')
                GROUP BY i.unidad""").fetchall())
        if by_unit:
            fig = go.Figure(data=[go.Bar(
                x=[u["unidad"] for u in by_unit],
                y=[round(u["avg_estres"], 1) for u in by_unit],
                marker_color=[GREEN if u["avg_estres"] < 3
                              else YELLOW if u["avg_estres"] < 4
                              else RED for u in by_unit])])
            fig.update_layout(height=300, yaxis=dict(range=[0, 5.5]),
                              yaxis_title="Estrés Promedio")
            st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════
    # TAB 2: GESTIONAR COLABORADORES
    # ══════════════════════════════════════
    with tab2:
        st.markdown("### 👥 Todos los Colaboradores")

        all_users = db.get_all_users_admin()
        activos = [u for u in all_users if u["estado"] == "Activo"]
        inactivos = [u for u in all_users if u["estado"] != "Activo"]

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("✅ Activos", len(activos), color=GREEN)
        with c2:
            metric_card("❌ Inactivos", len(inactivos), color=RED)
        with c3:
            metric_card("📋 Total", len(all_users), color=TURQ)

        # Filtros
        units = ["Todas"] + db.get_units()
        filter_unit = st.selectbox("Filtrar por unidad:", units, key="admin_filter_unit")
        filter_estado = st.radio("Estado:", ["Activos", "Inactivos", "Todos"],
                                 horizontal=True, key="admin_filter_estado")

        filtered = all_users
        if filter_unit != "Todas":
            filtered = [u for u in filtered if u.get("unidad") == filter_unit]
        if filter_estado == "Activos":
            filtered = [u for u in filtered if u["estado"] == "Activo"]
        elif filter_estado == "Inactivos":
            filtered = [u for u in filtered if u["estado"] != "Activo"]

        st.caption(f"Mostrando {len(filtered)} colaboradores")

        for u in filtered:
            is_active = u["estado"] == "Activo"
            icon = "🟢" if is_active else "🔴"

            with st.expander(f"{icon} {u['nombre']} — {u.get('unidad', '')} · {u['rol']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Email:** {u['email']}")
                    st.markdown(f"**Cargo:** {u.get('puesto', '—')}")
                    st.markdown(f"**Unidad:** {u.get('unidad', '—')}")
                with c2:
                    st.markdown(f"**Rol:** {u['rol']}")
                    st.markdown(f"**Teléfono:** {u.get('telefono', '—')}")
                    st.markdown(f"**Ingreso:** {u.get('fecha_ingreso', '—')}")

                st.divider()

                st.markdown("**✏️ Editar:**")
                col1, col2, col3 = st.columns(3)
                new_rol = col1.selectbox("Rol", ROLES,
                    index=ROLES.index(u["rol"]) if u["rol"] in ROLES else 3,
                    key=f"rol_{u['email']}")
                new_unidad = col2.text_input("Unidad", value=u.get("unidad", ""),
                    key=f"uni_{u['email']}")
                new_puesto = col3.text_input("Cargo", value=u.get("puesto", ""),
                    key=f"pue_{u['email']}")

                bc1, bc2, bc3 = st.columns(3)
                with bc1:
                    if st.button("💾 Guardar cambios", key=f"save_{u['email']}"):
                        db.update_colaborador(u["email"],
                            rol=new_rol, unidad=new_unidad, puesto=new_puesto)
                        st.success("Actualizado")
                        st.rerun()
                with bc2:
                    if is_active:
                        if st.button("❌ Desactivar", key=f"deact_{u['email']}"):
                            db.deactivate_colaborador(u["email"])
                            st.warning(f"{u['nombre']} desactivado")
                            st.rerun()
                    else:
                        if st.button("✅ Reactivar", key=f"react_{u['email']}"):
                            db.reactivate_colaborador(u["email"])
                            st.success(f"{u['nombre']} reactivado")
                            st.rerun()
                with bc3:
                    if st.button("🔑 Resetear clave", key=f"reset_{u['email']}"):
                        db.reset_password(u["email"])
                        st.info("Contraseña reseteada a Itaca2026!")

    # ══════════════════════════════════════
    # TAB 3: AGREGAR NUEVO COLABORADOR
    # ══════════════════════════════════════
    with tab3:
        st.markdown("### ➕ Agregar Nuevo Colaborador")
        st.caption("El nuevo colaborador recibirá la contraseña temporal `Itaca2026!` "
                   "y deberá cambiarla en su primer login.")

        with st.form("add_user_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_email = st.text_input("📧 Email (será su usuario de login)",
                    placeholder="nombre@gmail.com")
                new_nombre = st.text_input("👤 Nombre completo",
                    placeholder="María García")
                new_rol = st.selectbox("🎭 Rol", ROLES, index=3)
                new_cargo = st.text_input("💼 Cargo",
                    placeholder="Psicóloga")
            with c2:
                existing_units = db.get_units()
                unit_options = existing_units + ["(Otra)"]
                new_unidad = st.selectbox("🏢 Unidad", unit_options)
                if new_unidad == "(Otra)":
                    new_unidad = st.text_input("Nueva unidad:")

                leaders = [u for u in db.get_all_users()
                           if u["rol"] in ("Líder", "Admin", "Coordinador")]
                leader_opts = ["(Sin líder)"] + [f"{l['nombre']} ({l['email']})"
                                                 for l in leaders]
                leader_sel = st.selectbox("👑 Líder directo", leader_opts)
                new_lider = None
                if leader_sel != "(Sin líder)":
                    new_lider = leader_sel.split("(")[1].rstrip(")")

                new_tel = st.text_input("📱 Teléfono", placeholder="999888777")
                new_ingreso = st.date_input("📅 Fecha de ingreso")

            if st.form_submit_button("✅ Agregar Colaborador", type="primary"):
                if not new_email or not new_nombre:
                    st.error("Email y nombre son obligatorios.")
                elif "@" not in new_email:
                    st.error("Ingresa un email válido.")
                else:
                    ok, msg = db.add_colaborador(
                        email=new_email.lower().strip(),
                        nombre=new_nombre.strip(),
                        rol=new_rol,
                        unidad=new_unidad,
                        email_lider=new_lider,
                        cargo=new_cargo,
                        telefono=new_tel,
                        fecha_ingreso=new_ingreso.isoformat() if new_ingreso else ""
                    )
                    if ok:
                        st.success(msg)
                        st.balloons()
                    else:
                        st.error(msg)

    # ══════════════════════════════════════
    # TAB 4: HERRAMIENTAS
    # ══════════════════════════════════════
    with tab4:
        st.markdown("### 🔧 Herramientas de Administración")

        st.markdown("#### 📊 Resumen por Unidad")
        with db.get_db() as conn:
            by_unit_summary = db.dict_rows(conn.execute("""
                SELECT unidad, COUNT(*) as total,
                       SUM(CASE WHEN estado='Activo' THEN 1 ELSE 0 END) as activos,
                       SUM(CASE WHEN rol='Líder' THEN 1 ELSE 0 END) as lideres
                FROM usuarios WHERE unidad IS NOT NULL AND unidad != ''
                GROUP BY unidad ORDER BY unidad""").fetchall())
        if by_unit_summary:
            import pandas as pd
            df = pd.DataFrame(by_unit_summary)
            st.dataframe(df.rename(columns={
                "unidad": "Unidad", "total": "Total", "activos": "Activos",
                "lideres": "Líderes"}), use_container_width=True)

        st.divider()

        st.markdown("#### 📋 Resumen por Rol")
        with db.get_db() as conn:
            by_rol = db.dict_rows(conn.execute("""
                SELECT rol, COUNT(*) as total,
                       SUM(CASE WHEN estado='Activo' THEN 1 ELSE 0 END) as activos
                FROM usuarios GROUP BY rol ORDER BY rol""").fetchall())
        if by_rol:
            import pandas as pd
            df = pd.DataFrame(by_rol)
            st.dataframe(df.rename(columns={
                "rol": "Rol", "total": "Total", "activos": "Activos"
            }), use_container_width=True)

        st.divider()

        st.markdown("#### 🔑 Resetear contraseña masivo")
        st.caption("Resetea la clave de TODOS los usuarios a `Itaca2026!`")
        if st.button("🔑 Resetear TODAS las contraseñas", type="secondary"):
            with db.get_db() as conn:
                conn.execute("UPDATE usuarios SET password='Itaca2026!'")
            st.warning("Todas las contraseñas han sido reseteadas.")
