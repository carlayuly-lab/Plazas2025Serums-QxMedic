import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Beta 1 - QX Medic SERUMS", layout="wide", page_icon="🏥")

# Estilo CSS para tarjetas limpias
st.markdown("""
    <style>
    .main-card { 
        background-color: white; border: 1px solid #e6e9ef; padding: 20px; 
        border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 6px solid #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para convertir URL de Panopto a Embed
def get_panopto_embed_url(url):
    if pd.isna(url) or url == '': return None
    return str(url).replace("Viewer.aspx", "Embed.aspx")

# --- 2. INTERFAZ Y LÓGICA ---
st.title("🏥 Beta 1: Gestión de Plazas SERUMS 2025")
archivo = st.file_uploader("📂 Carga tu archivo INFO.csv", type=["csv"])

if archivo is not None:
    # Lectura del archivo (asegurando el delimitador ;)
    df = pd.read_csv(archivo, sep=';')
    df.columns = [c.strip() for c in df.columns]

    # Sidebar: Filtros
    st.sidebar.header("🔍 Panel de Filtros")
    depto_sel = st.sidebar.multiselect("Departamentos", options=sorted(df['DEPARTAMENTO'].unique()))
    grado_sel = st.sidebar.multiselect("Grado de Dificultad", options=sorted(df['GRADO DE DIFICULTAD'].unique()))

    # Aplicación de filtros
    df_f = df.copy()
    if depto_sel: df_f = df_f[df_f['DEPARTAMENTO'].isin(depto_sel)]
    if grado_sel: df_f = df_f[df_f['GRADO DE DIFICULTAD'].isin(grado_sel)]

    # Resultados
    st.subheader(f"📊 Resultados: {len(df_f)}")
    
    for _, row in df_f.iterrows():
        embed_url = get_panopto_embed_url(row.get('TESTIMONIOS'))
        
        # Tarjeta de información
        with st.container():
            st.markdown(f"""
                <div class="main-card">
                    <h3>🏥 {row['NOMBRE DE ESTABLECIMIENTO']}</h3>
                    <p><b>📍 Ubicación:</b> {row['DISTRITO']}, {row['PROVINCIA']} ({row['DEPARTAMENTO']})</p>
                    <p><b>🛡️ Dificultad:</b> {row['GRADO DE DIFICULTAD']} | <b>Categoría:</b> {row['CATEGORÍA']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # --- VIDEO DIRECTO (SIN EXPANDERS) ---
            if embed_url:
                st.markdown("**🎥 Testimonio de la sede:**")
                components.iframe(embed_url, height=350, scrolling=False)
            else:
                st.info("ℹ️ Sin video disponible para esta sede.")
            
            st.markdown("---") # Separador visual

else:
    st.warning("⚠️ Por favor, sube el archivo INFO.csv para activar el visor.")