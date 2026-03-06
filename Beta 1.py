import streamlit.components.v1 as components
from urllib.parse import urlparse, urlunparse

def get_panopto_embed_url(url):
    """
    Transforma una URL de visualización de Panopto a una URL de embed.
    """
    if "Panopto/Pages/Viewer.aspx" in url:
        return url.replace("Viewer.aspx", "Embed.aspx")
    return url

# --- 5. SECCIÓN DE TESTIMONIOS ---
st.markdown("---")
st.subheader("🎓 Testimonios: Experiencia SERUMS")

# Entrada para el link del video
link_video = st.text_input("🔗 Pega el enlace del video de Panopto:", 
                           placeholder="Ej: https://grupomedicoprometeo.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=...")

if link_video:
    try:
        embed_url = get_panopto_embed_url(link_video)
        
        # Renderizado del video
        components.iframe(embed_url, height=450, scrolling=False)
        st.caption("Nota: Asegúrate de que el video tenga los permisos de acceso configurados como 'Público' o 'Cualquier persona con el enlace' en Panopto para que se visualice correctamente.")
    except Exception as e:
        st.error("No se pudo cargar el video. Por favor, verifica el enlace.")