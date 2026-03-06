import streamlit as st
import pandas as pd

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Beta 1 - Dashboard SERUMS", layout="wide", page_icon="🏥")

# Estilo CSS para las tarjetas en cuadrícula
st.markdown("""
    <style>
    .card { 
        background-color: #ffffff; border: 1px solid #e1e4e8; padding: 20px; 
        border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CARGA DE DATOS DESDE GITHUB ---
@st.cache_data(ttl=600)
def cargar_datos_github():
    # Asegúrate de que esta URL sea la versión "Raw" de tu archivo INFO.csv en GitHub
    url = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/INFO.csv"
    df = pd.read_csv(url, sep=';')
    # Limpiamos los nombres de las columnas para evitar errores de espacios
    df.columns = [c.strip() for c in df.columns]
    return df

# --- 3. INTERFAZ ---
st.title("🏥 Dashboard de Plazas SERUMS 2025")

try:
    df = cargar_datos_github()

    # Sidebar: Filtros basados en las columnas del CSV
    st.sidebar.header("🔍 Filtros de Búsqueda")
    depto_sel = st.sidebar.multiselect("Departamentos", options=sorted(df['DEPARTAMENTO'].unique()))
    grado_sel = st.sidebar.multiselect("Grado de Dificultad", options=sorted(df['GRADO DE DIFICULTAD'].unique()))

    # Aplicación de filtros
    df_f = df.copy()
    if depto_sel: df_f = df_f[df_f['DEPARTAMENTO'].isin(depto_sel)]
    if grado_sel: df_f = df_f[df_f['GRADO DE DIFICULTAD'].isin(grado_sel)]

    # Métricas superiores
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Plazas", len(df_f))
    col_m2.metric("Con Testimonio", df_f['TESTIMONIOS'].notna().sum())
    col_m3.metric("Departamentos", len(df_f['DEPARTAMENTO'].unique()))

    st.markdown("---")

    # Grid de tarjetas (2 columnas)
    for i in range(0, len(df_f), 2):
        row = df_f.iloc[i:i+2]
        cols = st.columns(2)
        
        for idx, (_, item) in enumerate(row.iterrows()):
            with cols[idx]:
                # Renderizado de la tarjeta con datos del CSV
                st.markdown(f"""
                    <div class="card">
                        <h4 style='color: #1f77b4;'>{item['NOMBRE DE ESTABLECIMIENTO']}</h4>
                        <p><b>📍 {item['DISTRITO']}, {item['DEPARTAMENTO']}</b></p>
                        <p>🛡️ <i>{item['GRADO DE DIFICULTAD']} | {item['CATEGORÍA']}</i></p>
                    </div>
                """, unsafe_allow_html=True)
                
                # --- BOTÓN PARA PANOPTO (SOLUCIÓN FIABLE) ---
                url_video = item.get('TESTIMONIOS')
                if pd.notna(url_video) and str(url_video).strip() != "":
                    st.link_button("🎥 Ver Testimonio Completo", url_video, use_container_width=True)
                else:
                    st.warning("ℹ️ Sin testimonio disponible.")
                
                st.write("") # Espaciado

except Exception as e:
    st.error(f"Error al cargar los datos desde GitHub: {e}")