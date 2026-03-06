import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Beta 1 - QX Medic SERUMS", layout="wide", page_icon="🏥")

st.markdown("""
    <style>
    .main-card { 
        background-color: white; border: 1px solid #e6e9ef; padding: 20px; 
        border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 6px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para convertir URL de Panopto
def get_panopto_embed_url(url):
    if pd.isna(url) or url == '': return None
    return str(url).replace("Viewer.aspx", "Embed.aspx")

# --- 2. CARGA DE DATOS (DESDE GITHUB) ---
@st.cache_data(ttl=600)
def cargar_datos():
    # REEMPLAZA CON TU URL RAW DE GITHUB
    url = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/INFO.csv"
    df = pd.read_csv(url, sep=';')
    df.columns = [c.strip() for c in df.columns]
    return df

# --- 3. INTERFAZ ---
st.title("🏥 Beta 1: Gestión de Plazas SERUMS 2025")

try:
    df = cargar_datos()

    # Sidebar: Filtros
    st.sidebar.header("🔍 Panel de Filtros")
    depto_sel = st.sidebar.multiselect("Departamentos", options=sorted(df['DEPARTAMENTO'].unique()))
    grado_sel = st.sidebar.multiselect("Grado de Dificultad", options=sorted(df['GRADO DE DIFICULTAD'].unique()))

    # Filtros
    df_f = df.copy()
    if depto_sel: df_f = df_f[df_f['DEPARTAMENTO'].isin(depto_sel)]
    if grado_sel: df_f = df_f[df_f['GRADO DE DIFICULTAD'].isin(grado_sel)]

    st.subheader(f"📊 Resultados encontrados: {len(df_f)}")
    
    for _, row in df_f.iterrows():
        embed_url = get_panopto_embed_url(row.get('TESTIMONIOS'))
        
        with st.container():
            st.markdown(f"""
                <div class="main-card">
                    <h3>🏥 {row['NOMBRE DE ESTABLECIMIENTO']}</h3>
                    <p><b>📍 Ubicación:</b> {row['DISTRITO']}, {row['PROVINCIA']} ({row['DEPARTAMENTO']})</p>
                    <p><b>🛡️ Dificultad:</b> {row['GRADO DE DIFICULTAD']} | <b>Categoría:</b> {row['CATEGORÍA']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- SOLUCIÓN PARA PANOPTO ---
            if embed_url:
                # Usamos link_button para evitar el bloqueo del iframe
                st.link_button("🎥 Ver Testimonio de la sede", embed_url, use_container_width=True)
            else:
                st.info("ℹ️ Sin video disponible para esta sede.")
            
            st.markdown("---") 

except Exception as e:
    st.warning("⚠️ Esperando datos desde GitHub o el archivo no está accesible.")