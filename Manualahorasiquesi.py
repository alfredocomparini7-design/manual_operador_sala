import os
import streamlit as st
from docx import Document
from PIL import Image

st.set_page_config(page_title="Manual Operador Super10", page_icon="🛒", layout="wide")

st.title("📘 Manual Operador Sala / Super10")
st.markdown("Versión interactiva con secciones jerárquicas, iconos e imágenes de apoyo.")

# --- Cargar DOCX desde el repo ---
doc_path = os.path.join(os.path.dirname(__file__), "manual.docx.docx")

try:
    doc = Document(doc_path)
    st.success("✅ Manual cargado correctamente")
except Exception:
    st.error("❌ No se pudo abrir el manual. Asegúrate de subir el `.docx` al repo.")
    st.stop()

# --- Definir iconos / imágenes por gran sección ---
ICONOS = {
    "caja": "caja.png",
    "sala": "sala.png",
    "supermercado": "supermercado.png",
    "carnicería": "carniceria.png"
}


# --- Función para mostrar subsecciones ---
def mostrar_seccion(titulo, contenido, allow_upload=False):
    with st.expander(f"📄 {titulo}", expanded=False):
        for linea in contenido:
            if linea.startswith("✅"):
                st.success(linea)
                if allow_upload:
                    ok_file = st.file_uploader(f"Sube ejemplo CORRECTO para {titulo}", type=["jpg","png"], key=f"ok_{titulo}")
                    if ok_file:
                        st.image(Image.open(ok_file), caption=f"✅ Correcto en {titulo}", use_column_width=True)
            elif linea.startswith("❌"):
                st.error(linea)
                if allow_upload:
                    bad_file = st.file_uploader(f"Sube ejemplo INCORRECTO para {titulo}", type=["jpg","png"], key=f"bad_{titulo}")
                    if bad_file:
                        st.image(Image.open(bad_file), caption=f"❌ Incorrecto en {titulo}", use_column_width=True)
            else:
                st.write(linea)

# --- Definir estructura de grandes secciones y subsecciones ---
GRANDES_SECCIONES = {
    "caja": ["impresora", "pagos"],
    "sala": ["mermas", "códigos de mermas", "cómo reponer"],
    "carnicería": ["equipos", "tipos de cortes"]
}

secciones = {}
seccion_actual = None
subseccion_actual = None

for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue

    t_lower = text.lower()

    # Detectar gran sección
    for gsec, subsecs in GRANDES_SECCIONES.items():
        if t_lower.startswith(gsec):
            seccion_actual = text
            subseccion_actual = None
            secciones[seccion_actual] = {}
            continue

    # Detectar subsección
    if seccion_actual:
        for sub in GRANDES_SECCIONES.get(seccion_actual.lower(), []):
            if t_lower.startswith(sub):
                subseccion_actual = text
                secciones[seccion_actual][subseccion_actual] = []
                break
        else:
            if subseccion_actual:
                secciones[seccion_actual][subseccion_actual].append(text)
            else:
                if "_general" not in secciones[seccion_actual]:
                    secciones[seccion_actual]["_general"] = []
                secciones[seccion_actual]["_general"].append(text)

# --- Renderizar secciones jerárquicas ---
for gsec, subsecs in secciones.items():
    col1, col2 = st.columns([1, 4])
    with col1:
        icon_path = ICONOS.get(gsec.lower())
        if icon_path and os.path.exists(os.path.join(os.path.dirname(__file__), icon_path)):
            st.image(os.path.join(os.path.dirname(__file__), icon_path), width=80)
        else:
            st.write("📌")
    with col2:
        st.header(gsec)

    # Renderizar subsecciones
    for ssec, contenido in subsecs.items():
        if ssec == "_general":
            mostrar_seccion(ssec, contenido, allow_upload=False)
        else:
            if "reponer" in ssec.lower() or "cortes" in ssec.lower():
                mostrar_seccion(ssec, contenido, allow_upload=True)
            else:
                mostrar_seccion(ssec, contenido, allow_upload=False)

# --- Extra: sección Tipos de cortes con imágenes ---
if "carnicería" in secciones:
    st.subheader("🔪 Tipos de cortes (ejemplo práctico)")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Corte 1")
        img1 = st.file_uploader("Subir imagen Corte 1", type=["jpg","png"], key="c1")
        if img1:
            st.image(Image.open(img1), caption="Corte 1", use_column_width=True)
            st.success("✅ Bien hecho")
        else:
            st.error("❌ Falta imagen")

    with col2:
        st.subheader("Corte 2")
        img2 = st.file_uploader("Subir imagen Corte 2", type=["jpg","png"], key="c2")
        if img2:
            st.image(Image.open(img2), caption="Corte 2", use_column_width=True)
            st.success("✅ Bien hecho")
        else:
            st.error("❌ Falta imagen")









