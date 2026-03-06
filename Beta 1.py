import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Beta 1 - QX Medic SERUMS", layout="wide", page_icon="🏥")

# Estilo CSS
st.markdown("""
    <style>
    .reportview-container { background: #f5f7f9; }
    .main-card { 
        background-color: white;
        border: 1px solid #e6e9ef; 
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 6px solid #1f77b4;
    }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Función Helper Panopto
def get_panopto_embed_url(url):
    if "Panopto/Pages/Viewer.aspx" in url:
        return url.replace("Viewer.aspx", "Embed.aspx")
    return url

# Función Lógica Procesamiento
def enriquecer_datos(row):
    dept = str(row.get('DEPARTAMENTO', '')).upper()
    dif = str(row.get('GRADO DE DIFICULTAD', ''))
    
    if 'LIMA' in dept: dist = np.random.randint(20, 160)
    elif any(d in dept for d in ['AMAZONAS', 'LORETO', 'UCAYALI']): dist = np.random.randint(900, 1600)
    else: dist = np.random.randint(300, 850)
    
    transp = "Avión + Lancha" if dist > 900 else "Bus Interprovincial"
    es_rural = any(g in dif for g in ['GD-4', 'GD-5'])
    
    return pd.Series([
        dist, transp, 
        "Rural" if es_rural else "Urbano",
        "Panel Solar" if es_rural else "Red Eléctrica",
        "Pozo/Río" if es_rural else "Agua Potable",
        f"Ruta sugerida: {transp} hasta capital regional."
    ])

# --- 2. INTERFAZ ---
st.title("🏥 Beta 1: Gestión de Plazas SERUMS 2025")
st.caption("Asistente Virtual para QX Medic")

col_file, col_info = st.columns([2, 1])
with col_file:
    archivo = st.file_uploader("📂 Carga tu archivo INFO.csv aquí", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo, sep=';')
    df.columns = [c.replace('\n', ' ').strip() for c in df.columns]
    
    cols_nuevas = ['DISTANCIA_KM', 'TRANSPORTE', 'ZONA', 'LUZ', 'AGUA', 'COMO_LLEGAR']
    df[cols_nuevas] = df.apply(enriquecer_datos, axis=1)

    # Sidebar
    st.sidebar.image("https://www.qxmedic.com/wp-content/uploads/2021/07/logo-qxmedic-300x74.png", width=200)
    st.sidebar.header("🔍 Panel de Filtros")
    busqueda = st.sidebar.text_input("Buscar Establecimiento", placeholder="Ej: Puesto de Salud...")
    depto_sel = st.sidebar.multiselect("Departamentos", options=sorted(df['DEPARTAMENTO'].unique()))
    grado_sel = st.sidebar.multiselect("Grado de Dificultad", options=sorted(df['GRADO DE DIFICULTAD'].unique()))

    # Filtros
    df_f = df.copy()
    if busqueda: df_f = df_f[df_f['NOMBRE DE ESTABLECIMIENTO'].str.contains(busqueda, case=False, na=False)]
    if depto_sel: df_f = df_f[df_f['DEPARTAMENTO'].isin(depto_sel)]
    if grado_sel: df_f = df_f[df_f['GRADO DE DIFICULTAD'].isin(grado_sel)]

    # Resultados
    st.subheader(f"📊 Resultados encontrados: {len(df_f)}")
    
    with st.expander("👁️ Ver tabla completa de datos"):
        st.dataframe(df_f, use_container_width=True)

    st.markdown("---")
    for _, row in df_f.iterrows():
        st.markdown(f"""
            <div class="main-card">
                <h3 style='margin-top:0;'>🏥 {row['NOMBRE DE ESTABLECIMIENTO']}</h3>
                <p><b>📍 Ubicación:</b> {row['DISTRITO']}, {row['PROVINCIA']} ({row['DEPARTAMENTO']})</p>
                <p><b>🛡️ Dificultad:</b> {row['GRADO DE DIFICULTAD']} | <b>Acceso:</b> {row['TRANSPORTE']} ({row['DISTANCIA_KM']} KM)</p>
            </div>
        """, unsafe_allow_html=True)

    # --- 3. SECCIÓN TESTIMONIOS ---
    st.markdown("---")
    st.subheader("🎓 Testimonios: Experiencia SERUMS")
    link_video = st.text_input("🔗 Pega el enlace de Panopto:", placeholder="Ej: https://grupomedicoprometeo.hosted.panopto.com/...")
    
    if link_video:
        embed_url = get_panopto_embed_url(link_video)
        components.iframe(embed_url, height=450, scrolling=False)

else:
    st.warning("⚠️ Por favor, sube el archivo INFO.csv para activar el visor.")