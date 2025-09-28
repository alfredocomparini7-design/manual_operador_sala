import os
import streamlit as st
from docx import Document
from PIL import Image

st.set_page_config(page_title="Manual Operador Super10", page_icon="🛒", layout="wide")

# --- Iconos por sección ---
ICONOS = {
    "caja": "📦",
    "impresora": "🖨️",
    "precios": "🏷️",
    "retornables": "♻️",
    "pagos": "💳",
    "sala": "🏬",
    "mermas": "🗑️",
    "carnicería": "🥩",
    "equipos": "⚙️",
    "extras": "📌",
    "cómo reponer": "🔄",
    "tipos de cortes": "🔪"
}

# --- Cargar DOCX ---
doc_path = os.path.join(os.path.dirname(__file__), "manual.docx.docx")
doc = Document(doc_path)

st.title("📘 Manual Operador Sala / Super10")
st.markdown("Versión interactiva con iconos, secciones separadas y ejemplos visuales.")

# --- Función para mostrar secciones ---
def mostrar_seccion(titulo, contenido):
    icono = "📄"
    for clave, ico in ICONOS.items():
        if clave in titulo.lower():
            icono = ico
            break
    with st.expander(f"{icono} {titulo}", expanded=False):
        for linea in contenido:
            if linea.startswith("✅"):
                st.success(linea)
            elif linea.startswith("❌"):
                st.error(linea)
            else:
                st.write(linea)

# --- Agrupar párrafos por secciones ---
seccion_actual = "General"
contenido = []

for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue

    # Detectar posibles títulos de sección
    if text.lower().startswith(tuple(ICONOS.keys())) or "Sala / Bodega" in text or "Carnicería" in text:
        # Mostrar la sección anterior
        if contenido:
            mostrar_seccion(seccion_actual, contenido)
            contenido = []
        seccion_actual = text
    else:
        contenido.append(text)

# Mostrar última sección
if contenido:
    mostrar_seccion(seccion_actual, contenido)

# --- Sección especial: fotos ---
st.markdown("## 📸 Ejemplos visuales")

col1, col2 = st.columns(2)
with col1:
    if os.path.exists(os.path.join(os.path.dirname(__file__), "Si.jpg")):
        st.image("Si.jpg", caption="✅ Así debería quedar", use_column_width=True)
    else:
        st.warning("Falta imagen 'Si.jpg' en el repositorio")

with col2:
    st.image(Image.new("RGB", (400, 300), color="lightgray"), caption="❌ Esto no es así (pendiente)")

# --- Sección Tipos de cortes ---
st.markdown("## 🔪 Tipos de cortes")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Corte 1")
    st.image(Image.new("RGB", (400, 200), color="lightgray"), caption="Espacio reservado")

with col2:
    st.subheader("Corte 2")
    st.image(Image.new("RGB", (400, 200), color="lightgray"), caption="Espacio reservado")






