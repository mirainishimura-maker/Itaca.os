"""
Ítaca OS 2.0 - Base de Datos SQLite
Todas las tablas, seed data, y operaciones CRUD
"""
import sqlite3, json, os
from datetime import datetime, timedelta, date
from contextlib import contextmanager

# Robust path that works in Streamlit Cloud, local, and any CWD
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_THIS_DIR, "data", "itaca.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def dict_row(row):
    return dict(row) if row else None

def dict_rows(rows):
    return [dict(r) for r in rows]

# ═══════════════════════════════════════════
# CREAR TABLAS
# ═══════════════════════════════════════════
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            email TEXT PRIMARY KEY, 
            nombre TEXT, 
            rol TEXT DEFAULT 'Colaborador',
            estado TEXT DEFAULT 'Activo', 
            unidad TEXT, 
            email_lider TEXT,
            password TEXT DEFAULT 'Itaca2026!', 
            fecha_registro TEXT, 
            ultimo_acceso TEXT
        );
        CREATE TABLE IF NOT EXISTS identidad (
            email TEXT PRIMARY KEY, nombre TEXT, foto_url TEXT, puesto TEXT,
            fecha_ingreso TEXT, rol TEXT, unidad TEXT, estado TEXT DEFAULT 'Activo',
            arquetipo_disc TEXT, disc_d INTEGER DEFAULT 0, disc_i INTEGER DEFAULT 0,
            disc_s INTEGER DEFAULT 0, disc_c INTEGER DEFAULT 0,
            meta_trascendente TEXT, frase_personal TEXT, limitantes TEXT,
            fortalezas TEXT, progreso_meta INTEGER DEFAULT 0, telefono TEXT,
            email_lider TEXT, fecha_actualizacion TEXT
        );
        CREATE TABLE IF NOT EXISTS metas (
            meta_id TEXT PRIMARY KEY, email TEXT, tipo TEXT, periodo TEXT,
            objetivo TEXT, kr1 TEXT, kr2 TEXT, kr3 TEXT,
            progreso INTEGER DEFAULT 0, estado TEXT DEFAULT 'Pendiente',
            fecha_creacion TEXT, fecha_limite TEXT
        );
        CREATE TABLE IF NOT EXISTS checkins (
            checkin_id TEXT PRIMARY KEY, email TEXT, estado_general TEXT,
            nivel_estres INTEGER, area_preocupacion TEXT, etiquetas TEXT,
            comentario TEXT, fecha TEXT, semana TEXT, alerta_enviada INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS faros (
            faro_id TEXT PRIMARY KEY, email_emisor TEXT, nombre_emisor TEXT,
            email_receptor TEXT, nombre_receptor TEXT, tipo_faro TEXT,
            pilar TEXT, animal TEXT, mensaje TEXT, foto_url TEXT,
            fecha_envio TEXT, estado TEXT DEFAULT 'Pendiente',
            email_aprobador TEXT, fecha_aprobacion TEXT,
            celebraciones INTEGER DEFAULT 0, visible INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS notificaciones (
            notif_id TEXT PRIMARY KEY, email_dest TEXT, tipo TEXT,
            titulo TEXT, mensaje TEXT, fecha TEXT,
            leida INTEGER DEFAULT 0, prioridad TEXT DEFAULT 'Media'
        );
        CREATE TABLE IF NOT EXISTS logros (
            logro_id TEXT PRIMARY KEY, email TEXT, badge_id TEXT,
            nombre_badge TEXT, descripcion TEXT, puntos INTEGER,
            categoria TEXT, fecha TEXT, icono TEXT
        );
        CREATE TABLE IF NOT EXISTS hexagono (
            eval_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, fecha TEXT,
            vision INTEGER, planificacion INTEGER, encaje INTEGER,
            entrenamiento INTEGER, evaluacion_mejora INTEGER, reconocimiento INTEGER,
            promedio REAL, reflexion TEXT, dim_baja TEXT, dim_alta TEXT
        );
        CREATE TABLE IF NOT EXISTS journal (
            journal_id TEXT PRIMARY KEY, email TEXT, fecha TEXT,
            emociones TEXT, intensidad INTEGER, trigger_text TEXT,
            pensamiento TEXT, reflexion TEXT, estrategia TEXT,
            efectividad INTEGER, contexto TEXT, dia_semana TEXT, hora_dia TEXT
        );
        CREATE TABLE IF NOT EXISTS brujula_eval (
            brujula_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, fecha TEXT,
            autoconocimiento INTEGER, autorregulacion INTEGER, motivacion INTEGER,
            empatia INTEGER, habilidades_sociales INTEGER,
            promedio REAL, comp_baja TEXT, comp_alta TEXT, reflexion TEXT,
            ejercicios_mes INTEGER DEFAULT 0, journal_mes INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ejercicios_log (
            log_id TEXT PRIMARY KEY, email TEXT, ejercicio_id TEXT,
            fecha TEXT, duracion_real INTEGER, efectividad INTEGER,
            estado_antes TEXT, estado_despues TEXT, notas TEXT, competencia TEXT
        );
        CREATE TABLE IF NOT EXISTS planes_accion (
            plan_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, dimension TEXT,
            puntaje_actual INTEGER, puntaje_meta INTEGER,
            accion1 TEXT, accion2 TEXT, accion3 TEXT,
            fecha_creacion TEXT, fecha_limite TEXT, estado TEXT DEFAULT 'Pendiente'
        );
        CREATE TABLE IF NOT EXISTS activity_log (
            log_id TEXT PRIMARY KEY, email TEXT, accion TEXT,
            detalle TEXT, fecha TEXT, modulo TEXT
        );
        """)
    seed_data()

# ═══════════════════════════════════════════
# SEED DATA
# ═══════════════════════════════════════════
def seed_data():
    with get_db() as db:
        c = db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        if c > 0:
            return
        now = datetime.now().isoformat()
        # ═══════════════════════════════════════════════════════
        # 90 COLABORADORES REALES DE ÍTACA HUB
        # Fuente: BD MAESTRA (Excel), Febrero 2026
        # Formato: (email, nombre, rol, estado, unidad, email_lider, cargo, celular, ingreso)
        # ═══════════════════════════════════════════════════════
        users = [
            ("oscar.bereche@itaca.com","Oscar Sebastián García Bereche","Colaborador","Activo","321 SHOW","francisco.orellano@itaca.com","Videógrafo","974585296","2021-03-15"),
            ("francisco.orellano@itaca.com","Francisco Javier Muñoz Orellano","Líder","Activo","321 SHOW",None,"Socio","969680096","2021-09-10"),
            ("max.jimenez@itaca.com","Max Angel Chero Jiménez","Líder","Activo","ARTAMAX",None,"Socio / Gerente","973355562","2025-04-01"),
            ("esther.ortiz@itaca.com","Esther Abigail Ayala Ortiz","Colaborador","Activo","ARTAMAX","max.jimenez@itaca.com","Docente","917827155","2025-08-01"),
            ("anthonella.ojeda@itaca.com","Anthonella Abigail Ojeda Ojeda","Colaborador","Activo","ARTAMAX","max.jimenez@itaca.com","Asistente Gerencial","929596616","2025-10-13"),
            ("jorge.romero@itaca.com","Jorge Augusto Lazarte Romero","Líder","Activo","B&J ASESORES",None,"Socio / Director","959300115","2022-01-01"),
            ("keiko.cordova@itaca.com","Keiko Danitza Ramos Córdova","Colaborador","Activo","B&J ASESORES","jorge.romero@itaca.com","Asistente Contable","962807609","2023-01-01"),
            ("sara.miranda@itaca.com","Sara Belen Romero Miranda","Colaborador","Activo","B&J ASESORES","jorge.romero@itaca.com","Auxiliar Contable","933673617","2024-10-01"),
            ("nestor.hernandez@itaca.com","Néstor Javier Chanduvi Hernández","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","913069605","2020-01-06"),
            ("emma.mendoza@itaca.com","Emma Elizabeth Curipuma Mendoza","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","999138246","2023-01-01"),
            ("ana.sacchetti@itaca.com","Ana Luz López Sacchetti","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","940176075","2023-12-15"),
            ("melani.oscco@itaca.com","Melani Ramirez Oscco","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","969533354","2025-04-01"),
            ("pamela.silvera@itaca.com","Pamela Victoria Revilla Silvera","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","980715859","2023-08-31"),
            ("ayvi.huaman@itaca.com","Ayvi Yamillette Reyes Huamán","Coordinador","Activo","CONVER LIMA",None,"Coordinadora","960711603","2024-10-21"),
            ("katia.avila@itaca.com","Katia Gianelly Briones Avila","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","989018532","2025-03-15"),
            ("meriveth.garcia@itaca.com","Meriveth Ay-Ling Rojas García","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","978361147","2025-04-01"),
            ("arlette.mestanza@itaca.com","Arlette Solange Santibañez Mestanza","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","998732273","2025-04-01"),
            ("paolo.camacho@itaca.com","Paolo Fabio Ronceros Camacho","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","936809795","2025-05-05"),
            ("camila.gamarra@itaca.com","Camila Fiorella Alvarez Gamarra","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","961891335","2025-06-01"),
            ("cristel.motta@itaca.com","Cristel Fiorella Ríos Motta","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","937091962","2025-06-01"),
            ("grecia.elera@itaca.com","Grecia Palacios Elera","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","962686617","2023-10-11"),
            ("alejandro.ortiz@itaca.com","Alejandro Chung Ortiz","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicólogo","968824862","2024-08-28"),
            ("joyce.mendoza@itaca.com","Joyce Calle Mendoza","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","995047598","2024-09-06"),
            ("yazmin.alvarado@itaca.com","Yazmin Fiorella Castillo Alvarado","Coordinador","Activo","CONVER PIURA",None,"Coordinadora","962840126","2025-01-02"),
            ("andrea.chirito@itaca.com","Andrea Elizabeth Cabellos Chirito","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","969214648","2025-01-30"),
            ("angi.vilela@itaca.com","Angi Lizeth Requena Vilela","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","958174225","2025-01-30"),
            ("maximo.espinoza@itaca.com","Maximo Jr. Aldana Espinoza","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicólogo","955667968","2025-06-16"),
            ("sofia.godinez@itaca.com","Sofía Isabel Ferreyra Godinez","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","991130790","2025-06-18"),
            ("inori.coronado@itaca.com","Inori Nishimura Coronado","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","970632478","2025-09-01"),
            ("maria.garcia@itaca.com","María Fernanda Vásquez García","Líder","Activo","ECO",None,"Directora y entrenadora","999642183","2025-04-02"),
            ("johana.sanchez@itaca.com","Johana Andrea Díaz Sanchez","Colaborador","Activo","ECO","maria.garcia@itaca.com","Docente","991403599","2025-08-01"),
            ("alvaro.gallo@itaca.com","Alvaro Alonso Gallo","Colaborador","Activo","ECO","maria.garcia@itaca.com","Docente","965788767","2025-08-01"),
            ("harold.arevalo@itaca.com","Harold Serhio Quinde Arévalo","Líder","Activo","ITACA EDUCACIÓN",None,"Entrenador / Director","901791803","2024-01-01"),
            ("maria.arechaga@itaca.com","María Carla Roxany Arrese Arechaga","Colaborador","Activo","ITACA EDUCACIÓN","harold.arevalo@itaca.com","Entrenadora","963777646","2024-01-01"),
            ("jadek.renteria@itaca.com","Jadek Renteria","Colaborador","Activo","ITACA EDUCACIÓN","harold.arevalo@itaca.com","Practicante","967384002","2025-07-14"),
            ("brandon.cordova@itaca.com","Brandon Skiev Soto Cordova","Líder","Activo","ITACA HUB",None,"Socio Ítaca Hub","951657082","2014-09-01"),
            ("brian.olaya@itaca.com","Brian Stefano Savitzky Olaya","Líder","Activo","ITACA HUB","brandon.cordova@itaca.com","Socio Ítaca Hub","944438905","2014-09-01"),
            ("mattias.savitzky@itaca.com","Mattias Mattos Savitzky","Coordinador","Activo","ITACA HUB","brandon.cordova@itaca.com","Coordinador administrativo","951201565","2022-01-06"),
            ("gabriel.savitzky@itaca.com","Gabriel Mattos Savitzky","Líder","Activo","ITACA HUB","brandon.cordova@itaca.com","Director comercial","922215252","2022-04-16"),
            ("astrid.vivas@itaca.com","Astrid Adanai Ramos Vivas","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Asistente Gerencial","957552519","2023-04-13"),
            ("jose.chuquicondor@itaca.com","José Piero Alexandro Zapata Chuquicondor","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Procesos administrativos","920129548","2023-12-11"),
            ("piero.garcia@itaca.com","Piero Huertas García","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Marketing","976216997","2024-03-01"),
            ("virginia.rabanal@itaca.com","Virginia Anaís Robledo Rabanal","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Asistente Gerencial","918406473","2024-09-01"),
            ("brando.juarez@itaca.com","Brando Augusto Franco Juárez","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Marketing","947057325","2024-09-01"),
            ("mirai.coronado@itaca.com","Mirai Nishimura Coronado","Admin","Activo","ITACA HUB","brandon.cordova@itaca.com","Gestora de Talento Humano","977668497","2025-01-01"),
            ("monica.rolando@itaca.com","Mónica Alejandra Rodríguez Rolando","Colaborador","Activo","KIDS AREQUIPA","gabriel.savitzky@itaca.com","Entrenadora Kids Arequipa","953850222","2024-08-31"),
            ("axlen.barra@itaca.com","Axlen Nicole Fernández Barra","Colaborador","Activo","KIDS AREQUIPA","gabriel.savitzky@itaca.com","Entrenadora Kids Arequipa","983754707","2024-08-31"),
            ("gabriela.juarez@itaca.com","Gabriela Lucía Rentería Juárez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Psicóloga","961350844","2019-01-02"),
            ("maria.ramirez@itaca.com","María de los Ángeles Espinoza Ramirez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids","912550185","2024-01-01"),
            ("luana.camacho@itaca.com","Luana Marialé Gallesi Camacho","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Co-entrenadora Kids Lima","913718440","2024-01-12"),
            ("gianela.lopez@itaca.com","Gianela Esther Loardo Lopez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids Lima","964240154","2024-04-12"),
            ("fernanda.cabrera@itaca.com","Fernanda Elizabeth Vizcarra Cabrera","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids Lima","980732705","2024-08-30"),
            ("giresse.castillo@itaca.com","Giresse Alexander Bernuy Castillo","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenador Kids Lima","947725759","2024-08-30"),
            ("adriana.alvarado@itaca.com","Adriana Ximena Harumy Díaz Alvarado","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Psicóloga","992837265","2024-08-30"),
            ("jesus.martinez@itaca.com","Jesús Israel Montellanos Martinez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenador Kids Lima","906837369","2024-08-31"),
            ("diana.aliaga@itaca.com","Diana Susana Cornejo Aliaga","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids","963781075","2024-12-13"),
            ("lucia.huambachano@itaca.com","Lucía Alessandra Meza Huambachano","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids Lima","",""),
            ("fransheska.atoche@itaca.com","Fransheska Teresa Saldarriaga Atoche","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids Piura","921988904","2020-07-01"),
            ("taiz.saucedo@itaca.com","Taiz Kasandra Ivonne Martinez Saucedo","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","994191006","2022-05-14"),
            ("candy.vera@itaca.com","Candy Alisson Huertas Vera","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","907851180","2023-09-01"),
            ("tatiana.cruz@itaca.com","Tatiana Milene Lachira Cruz","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids Piura","951933777","2024-04-11"),
            ("kristel.chunga@itaca.com","Kristel Rosa Saavedra Chunga","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","977195668","2024-04-27"),
            ("ana.iman@itaca.com","Ana Lucía Gallardo Imán","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","938310093","2024-09-01"),
            ("angie.morocho@itaca.com","Angie de los Milagros Salvador Morocho","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids Piura","953348766",""),
            ("victoria.valencia@itaca.com","Victoria María Rodríguez Valencia","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Psicóloga Kids","934637679",""),
            ("luisa.dolly@itaca.com","Luisa María Castillo Dolly","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","903003595",""),
            ("santiago.zambrano@itaca.com","Santiago Sánchez Zambrano","Líder","Activo","MARKETING",None,"Socio Ítaca Marketing","997754433","2020-01-11"),
            ("daniela.collantes@itaca.com","Daniela Fernanda Tocto Collantes","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Project Manager","944822543","2021-04-12"),
            ("edson.pena@itaca.com","Edson Martín Domínguez Peña","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Diseñador gráfico","978379477","2021-06-21"),
            ("jose.lecca@itaca.com","José Joaquín Murillo Lecca","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Entrenador Kids Lima","921168570","2024-01-08"),
            ("maickol.ayala@itaca.com","Maickol Yorvn Saavedra Ayala","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Creador de contenido","986982339","2024-01-12"),
            ("gabriel.querevalu@itaca.com","Gabriel Efraín Chavez Querevalu","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Analista de pauta","962082320","2024-11-04"),
            ("damaris.lupuche@itaca.com","Damaris Nicol Aguilar Lupuche","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Practicante CC","918135940","2024-11-04"),
            ("milagros.socola@itaca.com","Milagros Stephany Espinoza Socola","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante Hub","959247793","2025-08-28"),
            ("rodrigo.hurtado@itaca.com","Rodrigo Joaquín Cruz Hurtado","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante Marco Legal","961861390","2025-09-22"),
            ("jocelyn.vivas@itaca.com","Jocelyn Aradiel Ramos Vivas","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante Editora","920862467","2025-10-01"),
            ("claudia.chuquicondor@itaca.com","Claudia Belén Zapata Chuquicondor","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante RH","959143022","2025-12-15"),
            ("luis.sosa@itaca.com","Luis Alberto Chiroque Sosa","Líder","Activo","SOCIOS",None,"Socio Club de Arte y Cultura","943742516","2019-01-01"),
            ("nadia.olaya@itaca.com","Nadia Lissett Savitzky Olaya","Líder","Activo","SOCIOS",None,"Socia Ítaca Hub","978661349","2016-01-01"),
            ("eddie.cespedes@itaca.com","Eddie Raúl Valdiviezo Céspedes","Líder","Activo","SOCIOS",None,"Socio Ítaca Hub","958928102","2017-01-02"),
            ("keila.zegarra@itaca.com","Keila Cornejo Zegarra","Líder","Activo","SOCIOS",None,"Socia Club de Arte","929966010","2019-08-01"),
            ("luciana.calderon@itaca.com","Luciana Rubí Portilla Calderón","Líder","Activo","SOCIOS",None,"Socia Inversionista Kids Piura","991570706","2023-04-01"),
            ("brando.camacho@itaca.com","Brando Alonso Gallesi Camacho","Líder","Activo","SOCIOS",None,"Socio Ítaca Kids Lima","913066690","2023-12-31"),
            ("jesus.andrade@itaca.com","Jesús Andrade","Líder","Activo","SOCIOS",None,"Socio Ítaca Conversemos","954044292",""),
            ("nadia.echevarria@itaca.com","Nadia Susiré Herrera Echevarría","Líder","Activo","SOCIOS",None,"Socia Ítaca Kids Lima","964589249",""),
        ]
        for u in users:
            email, nombre, rol, estado, unidad, email_lider, cargo, cel, ingreso = u
            db.execute("INSERT OR IGNORE INTO usuarios VALUES (?,?,?,?,?,?,?,?)",
                (email, nombre, rol, estado, unidad, email_lider, now, now))
            db.execute("""INSERT OR IGNORE INTO identidad
                (email,nombre,puesto,rol,unidad,estado,email_lider,telefono,fecha_ingreso,fecha_actualizacion)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (email, nombre, cargo, rol, unidad, estado, email_lider, cel, ingreso, now))
        # Algunos check-ins de ejemplo
        for i, email in enumerate(["pedro@itaca.com","lucia@itaca.com","diego@itaca.com"]):
            for w in range(4):
                d = datetime.now() - timedelta(weeks=w)
                estados = ["GENIAL","NORMAL","DIFICIL","NORMAL"]
                estres = [2, 3, 4, 2]
                cid = f"{email}_{d.strftime('%Y-%m-%d')}"
                sem = f"{d.year}-S{d.isocalendar()[1]:02d}"
                db.execute("INSERT OR IGNORE INTO checkins VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (cid, email, estados[w], estres[w], "Trabajo", "Concentrado,Determinado",
                     "", d.isoformat(), sem, 1 if estres[w]>=4 else 0))
        # Faros de ejemplo con colaboradores reales
        faros_data = [
            ("astrid.vivas@itaca.com","Astrid Adanai Ramos Vivas","mirai.coronado@itaca.com","Mirai Nishimura Coronado","Faro de Valor","ITACTIVIDAD","Ardilla","Gracias por resolver el tema de contratos sin que nadie te lo pidiera. Eso es ITACTIVIDAD pura."),
            ("grecia.elera@itaca.com","Grecia Palacios Elera","yazmin.alvarado@itaca.com","Yazmin Fiorella Castillo Alvarado","Faro de Aliento","Muro de Confianza","Ganso","Sé que esta semana fue intensa con las consultas. Quiero que sepas que cuentas con todo el equipo."),
            ("daniela.collantes@itaca.com","Daniela Fernanda Tocto Collantes","santiago.zambrano@itaca.com","Santiago Sánchez Zambrano","Faro de Guía","+1 Sí Importa","Castor","Gracias por enseñarme a usar las métricas de pauta. Siempre das la milla extra."),
        ]
        for i, f in enumerate(faros_data):
            fid = f"FARO_{int(datetime.now().timestamp())}{i}"
            d = datetime.now() - timedelta(days=i*3)
            db.execute("INSERT OR IGNORE INTO faros VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (fid, f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], "",
                 d.isoformat(), "Aprobado", "mirai@itaca.com", d.isoformat(), 0, 1))
        # Badge de ejemplo
        db.execute("INSERT OR IGNORE INTO logros VALUES (?,?,?,?,?,?,?,?,?)",
            ("LOGRO_pedro_firstfaro", "pedro@itaca.com", "FIRST_FARO", "🔦 Primer Faro",
             "Encendiste tu primer faro", 10, "Cultura", now, "🔦"))

# ═══════════════════════════════════════════
# CRUD OPERATIONS
# ═══════════════════════════════════════════

# ── USUARIOS ──
def get_user(email):
    with get_db() as db:
        return dict_row(db.execute("SELECT * FROM usuarios WHERE email=?", (email,)).fetchone())

def get_all_users():
    with get_db() as db:
        return dict_rows(db.execute("SELECT * FROM usuarios WHERE estado='Activo' ORDER BY nombre").fetchall())

def get_identidad(email):
    with get_db() as db:
        return dict_row(db.execute("SELECT * FROM identidad WHERE email=?", (email,)).fetchone())

def update_identidad(email, **kwargs):
    with get_db() as db:
        sets = ", ".join(f"{k}=?" for k in kwargs)
        vals = list(kwargs.values()) + [email]
        db.execute(f"UPDATE identidad SET {sets}, fecha_actualizacion=? WHERE email=?",
                   (*kwargs.values(), datetime.now().isoformat(), email))

def get_team_members(email_lider):
    with get_db() as db:
        user = dict_row(db.execute("SELECT unidad FROM identidad WHERE email=?", (email_lider,)).fetchone())
        if not user: return []
        return dict_rows(db.execute(
            "SELECT * FROM identidad WHERE unidad=? AND email!=? AND estado='Activo'",
            (user["unidad"], email_lider)).fetchall())

# ── CHECK-INS ──
def save_checkin(email, estado, estres, area, etiquetas, comentario):
    now = datetime.now()
    cid = f"{email}_{now.strftime('%Y-%m-%d')}"
    sem = f"{now.year}-S{now.isocalendar()[1]:02d}"
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM checkins WHERE email=? AND semana=?", (email, sem)).fetchone()
        if existing:
            return False, "Ya hiciste tu check-in esta semana."
        db.execute("INSERT INTO checkins VALUES (?,?,?,?,?,?,?,?,?,?)",
            (cid, email, estado, estres, area, ",".join(etiquetas) if etiquetas else "",
             comentario, now.isoformat(), sem, 1 if estres >= 4 else 0))
    return True, "Check-in registrado. ¡Gracias por compartir!"

def get_my_checkins(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM checkins WHERE email=? ORDER BY fecha DESC LIMIT ?",
            (email, limit)).fetchall())

def get_team_checkins(email_lider):
    members = get_team_members(email_lider)
    if not members: return []
    emails = [m["email"] for m in members]
    ph = ",".join("?" * len(emails))
    with get_db() as db:
        return dict_rows(db.execute(f"""
            SELECT c.*, i.nombre FROM checkins c
            JOIN identidad i ON c.email = i.email
            WHERE c.email IN ({ph})
            ORDER BY c.fecha DESC LIMIT 50""", emails).fetchall())

def checkin_done_this_week(email):
    now = datetime.now()
    sem = f"{now.year}-S{now.isocalendar()[1]:02d}"
    with get_db() as db:
        return db.execute("SELECT 1 FROM checkins WHERE email=? AND semana=?", (email, sem)).fetchone() is not None

# ── FAROS ──
def save_faro(email_emisor, email_receptor, tipo_faro, mensaje):
    from config import TIPOS_FARO
    info = TIPOS_FARO[tipo_faro]
    now = datetime.now()
    fid = f"FARO_{int(now.timestamp())}"
    with get_db() as db:
        em = db.execute("SELECT nombre FROM identidad WHERE email=?", (email_emisor,)).fetchone()
        rc = db.execute("SELECT nombre FROM identidad WHERE email=?", (email_receptor,)).fetchone()
        nombre_e = em["nombre"] if em else email_emisor
        nombre_r = rc["nombre"] if rc else email_receptor
        db.execute("INSERT INTO faros VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (fid, email_emisor, nombre_e, email_receptor, nombre_r, tipo_faro,
             info["pilar"], info["animal"], mensaje, "", now.isoformat(),
             "Aprobado", "", now.isoformat(), 0, 1))
    return True, f"¡Faro enviado a {nombre_r}!"

def get_faros_recibidos(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM faros WHERE email_receptor=? AND visible=1 ORDER BY fecha_envio DESC LIMIT ?",
            (email, limit)).fetchall())

def get_faros_enviados(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM faros WHERE email_emisor=? ORDER BY fecha_envio DESC LIMIT ?",
            (email, limit)).fetchall())

def get_faros_publicos(limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM faros WHERE visible=1 ORDER BY fecha_envio DESC LIMIT ?",
            (limit,)).fetchall())

def celebrar_faro(faro_id):
    with get_db() as db:
        db.execute("UPDATE faros SET celebraciones = celebraciones + 1 WHERE faro_id=?", (faro_id,))

# ── HEXÁGONO ──
def save_hexagono(email, puntajes, reflexion):
    now = datetime.now()
    periodo = now.strftime("%Y-%m")
    eid = f"{email}_{periodo}"
    vals = list(puntajes.values())
    prom = round(sum(vals) / 6, 2)
    nombres = ["Visión Corporativa","Planificación","Encaje de Talento","Entrenamiento","Evaluación y Mejora","Reconocimiento"]
    dim_baja = nombres[vals.index(min(vals))]
    dim_alta = nombres[vals.index(max(vals))]
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM hexagono WHERE eval_id=?", (eid,)).fetchone()
        if existing:
            return False, "Ya evaluaste este mes."
        db.execute("INSERT INTO hexagono VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (eid, email, periodo, now.isoformat(), *vals, prom, reflexion, dim_baja, dim_alta))
    return True, f"Evaluación guardada. Promedio: {prom}"

def get_my_hexagono(email, limit=12):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM hexagono WHERE email=? ORDER BY periodo DESC LIMIT ?",
            (email, limit)).fetchall())

# ── JOURNAL ──
def save_journal(email, emociones, intensidad, trigger, pensamiento, reflexion, estrategia, efectividad, contexto):
    now = datetime.now()
    jid = f"{email}_{now.strftime('%Y-%m-%d_%H%M')}"
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    dia = dias[now.weekday()]
    hora = "Mañana" if now.hour < 12 else "Tarde" if now.hour < 18 else "Noche"
    with get_db() as db:
        db.execute("INSERT INTO journal VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (jid, email, now.isoformat(), ",".join(emociones), intensidad,
             trigger, pensamiento, reflexion, estrategia or "", efectividad or 0,
             contexto, dia, hora))
    return True, "Entrada de journal guardada."

def get_my_journal(email, limit=30):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM journal WHERE email=? ORDER BY fecha DESC LIMIT ?",
            (email, limit)).fetchall())

# ── BRÚJULA IE ──
def save_brujula(email, puntajes, reflexion):
    now = datetime.now()
    periodo = now.strftime("%Y-%m")
    bid = f"{email}_{periodo}"
    vals = list(puntajes.values())
    prom = round(sum(vals) / 5, 2)
    nombres = ["Autoconocimiento","Autorregulación","Motivación","Empatía","Habilidades Sociales"]
    comp_baja = nombres[vals.index(min(vals))]
    comp_alta = nombres[vals.index(max(vals))]
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM brujula_eval WHERE brujula_id=?", (bid,)).fetchone()
        if existing:
            return False, "Ya evaluaste este mes."
        ej_count = db.execute("SELECT COUNT(*) FROM ejercicios_log WHERE email=? AND fecha LIKE ?",
            (email, f"{periodo}%")).fetchone()[0]
        j_count = db.execute("SELECT COUNT(*) FROM journal WHERE email=? AND fecha LIKE ?",
            (email, f"{periodo}%")).fetchone()[0]
        db.execute("INSERT INTO brujula_eval VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (bid, email, periodo, now.isoformat(), *vals, prom, comp_baja, comp_alta,
             reflexion, ej_count, j_count))
    return True, f"Evaluación IE guardada. Promedio: {prom}"

def get_my_brujula(email, limit=12):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM brujula_eval WHERE email=? ORDER BY periodo DESC LIMIT ?",
            (email, limit)).fetchall())

# ── LOGROS ──
def get_my_logros(email):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM logros WHERE email=? ORDER BY fecha DESC", (email,)).fetchall())

def get_total_puntos(email):
    with get_db() as db:
        r = db.execute("SELECT COALESCE(SUM(puntos),0) FROM logros WHERE email=?", (email,)).fetchone()
        return r[0]

def otorgar_badge(email, badge_id, nombre, desc, puntos, categoria, icono):
    lid = f"LOGRO_{email.split('@')[0]}_{badge_id}"
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM logros WHERE logro_id=?", (lid,)).fetchone()
        if existing: return False
        db.execute("INSERT INTO logros VALUES (?,?,?,?,?,?,?,?,?)",
            (lid, email, badge_id, nombre, desc, puntos, categoria, datetime.now().isoformat(), icono))
    return True

# ── NOTIFICACIONES ──
def get_notificaciones(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM notificaciones WHERE email_dest=? ORDER BY fecha DESC LIMIT ?",
            (email, limit)).fetchall())

def count_unread(email):
    with get_db() as db:
        return db.execute("SELECT COUNT(*) FROM notificaciones WHERE email_dest=? AND leida=0",
            (email,)).fetchone()[0]

# ── ANALYTICS (Admin) ──
def get_analytics():
    with get_db() as db:
        total_users = db.execute("SELECT COUNT(*) FROM usuarios WHERE estado='Activo'").fetchone()[0]
        checkins_week = db.execute("SELECT COUNT(*) FROM checkins WHERE semana=?",
            (f"{datetime.now().year}-S{datetime.now().isocalendar()[1]:02d}",)).fetchone()[0]
        avg_estres = db.execute("SELECT AVG(nivel_estres) FROM checkins WHERE fecha > ?",
            ((datetime.now() - timedelta(days=7)).isoformat(),)).fetchone()[0] or 0
        alertas = db.execute("SELECT COUNT(*) FROM checkins WHERE alerta_enviada=1 AND fecha > ?",
            ((datetime.now() - timedelta(days=7)).isoformat(),)).fetchone()[0]
        faros_mes = db.execute("SELECT COUNT(*) FROM faros WHERE fecha_envio > ?",
            ((datetime.now() - timedelta(days=30)).isoformat(),)).fetchone()[0]
        total_faros = db.execute("SELECT COUNT(*) FROM faros").fetchone()[0]
        return {
            "total_users": total_users, "checkins_week": checkins_week,
            "avg_estres": round(avg_estres, 1), "alertas": alertas,
            "faros_mes": faros_mes, "total_faros": total_faros,
            "tasa_checkin": round((checkins_week / max(total_users, 1)) * 100),
        }

# Inicializar al importar
init_db()
