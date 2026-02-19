# ⚓ Ítaca OS 2.0

**Plataforma Integral de Gestión y Desarrollo Humano**

Aplicación web construida en Python + Streamlit para gestionar los 5 módulos de Ítaca Hub:

1. **Mi Esencia** — Perfil DISC + Meta Trascendente
2. **Mi Estrategia** — OKR + Metas
3. **Hexágono de Liderazgo** — 6 mínimos del líder
4. **Cultura Ítaca** — Check-ins + Faros + Pilares I+M + Gung Ho
5. **Brújula Emocional** — IE de Goleman + Journal + 22 Ejercicios

---

## 🚀 Instalación Rápida

### 1. Requisitos
- Python 3.9 o superior
- pip

### 2. Instalar dependencias
```bash
cd itaca-os
pip install -r requirements.txt
```

### 3. Ejecutar
```bash
streamlit run app.py
```

La app se abrirá en tu navegador en `http://localhost:8501`

---

## 📱 Usuarios de Prueba

La app viene con 8 usuarios precargados:

| Email | Nombre | Rol |
|-------|--------|-----|
| mirai@itaca.com | Mirai Gonzales | Admin |
| carlos@itaca.com | Carlos Mendoza | Líder |
| ana@itaca.com | Ana Torres | Líder |
| pedro@itaca.com | Pedro Ramírez | Colaborador |
| lucia@itaca.com | Lucía Fernández | Colaborador |
| diego@itaca.com | Diego Silva | Colaborador |
| maria@itaca.com | María López | Colaborador |
| jorge@itaca.com | Jorge Castillo | Coordinador |

Selecciona cualquier usuario en el sidebar para navegar como ese rol.

---

## 🏗️ Arquitectura

```
itaca-os/
├── app.py                 # Entrada principal
├── config.py              # Colores, constantes, pilares, competencias
├── database.py            # SQLite: 13 tablas, seed data, CRUD
├── requirements.txt
├── components/
│   ├── sidebar.py         # Navegación dinámica por rol
│   └── cards.py           # Componentes reutilizables (cards, charts)
├── pages/
│   ├── home.py            # Home Dashboard + Odisea
│   ├── mi_esencia.py      # Módulo 1
│   ├── mi_estrategia.py   # Módulo 2
│   ├── hexagono.py        # Módulo 3
│   ├── cultura.py         # Módulo 4
│   ├── brujula.py         # Módulo 5
│   ├── logros.py          # Gamificación
│   ├── notificaciones.py  # Centro de alertas
│   └── admin.py           # Dashboard Admin
└── data/
    ├── ejercicios.json    # 22 ejercicios de IE
    └── itaca.db           # SQLite (auto-generada)
```

---

## 🌐 Deploy en Streamlit Cloud (Gratis)

1. Sube el proyecto a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu repo
4. Main file: `app.py`
5. ¡Listo! Tu equipo accede desde el navegador

---

## 📋 Funcionalidades por Módulo

### Home Dashboard
- Saludo personalizado con hora
- Barra de progreso Odisea 2026 (6 olas)
- Botones CTA: Check-in + Faro
- Métricas rápidas (puntos, logros, estrés)
- Pulso del equipo (solo líderes)
- Muro público de faros

### Módulo 1: Mi Esencia
- Perfil completo editable
- Configuración DISC con puntajes D-I-S-C
- Meta Trascendente con barra de progreso
- Frase personal / mantra
- Tips de comunicación por DISC

### Módulo 2: Mi Estrategia
- Crear OKR con hasta 3 Key Results
- Actualizar progreso y estado
- Visualización por periodo

### Módulo 3: Hexágono de Liderazgo
- Radar chart de 6 dimensiones
- Autoevaluación mensual
- Evolución histórica
- Vista de Tripulación con check-ins

### Módulo 4: Cultura Ítaca
- Check-in semanal (estado, estrés, etiquetas, comentario)
- Enviar Faros (Valor/Guía/Aliento)
- Pilares I+M con Gung Ho (Ardilla/Castor/Ganso)
- Muro público con celebraciones
- Historial personal

### Módulo 5: Brújula Emocional
- Dashboard con radar de 5 competencias Goleman
- Journal emocional (emociones, triggers, reflexión)
- Catálogo de 22 ejercicios filtrable
- Autoevaluación mensual IE
- Evolución histórica con gráficas

### Gamificación
- Sistema de puntos y badges
- 9+ badges desbloqueables
- Niveles: Marinero → Navegante → Capitán → Almirante

### Admin Dashboard (solo Mirai)
- Métricas globales
- Check-ins de toda la organización
- Alertas de bienestar
- Distribución de faros por tipo
- Estrés por unidad
