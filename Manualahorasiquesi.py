from docx import Document
from PIL import Image
import streamlit as st

import os
from docx import Document

doc_path = os.path.join(os.path.dirname(__file__), "manual.docx.docx")
doc = Document(doc_path)


# --- Configuración de la app ---
st.set_page_config(page_title="Manual Operador Super10", page_icon="🛒", layout="wide")

st.title("📘 Manual de tareas - Operador Sala / Super10")
st.markdown("Versión interactiva y visual del manual, con ejemplos y espacios para imágenes.")

# --- Cargar documento Word ---
doc_path = "C:/Users/alfre/Downloads/manual.docx.docx"
doc = Document(doc_path)

# --- Renderizar secciones del documento ---
for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        st.write("")  # mantener espacios
        continue

    # Encabezados detectados
    if text.lower().startswith("caja") or text.lower().startswith("sala") or text.lower().startswith("cómo reponer") or text.lower().startswith("tipos de cortes"):
        st.subheader(text)
    elif text.startswith("✅"):
        st.success(text)
    elif text.startswith("❌"):
        st.error(text)
    else:
        st.write(text)

    # Sección especial: mostrar imagen en "Así debería quedar"
    if "Así debería quedar" in text:
        try:
            img = Image.open("Si.jpg")
            st.image(img, caption="Ejemplo correcto de reposición", use_column_width=True)
        except:
            st.warning("No se encontró la imagen de ejemplo (Si.jpg).")

    # Sección especial: subir imagen en "Esto no es así"
    if "Esto no es así" in text:
        file = st.file_uploader("Sube aquí un ejemplo de reposición incorrecta", type=["jpg","png"])
        if file:
            bad_img = Image.open(file)
            st.image(bad_img, caption="Ejemplo incorrecto de reposición", use_column_width=True)

# --- Nueva sección: Tipos de cortes ---
st.markdown("---")
st.header("🔪 Tipos de cortes")

st.write("A continuación se muestran espacios reservados para validar si un corte está **bien hecho (✅)** o **mal hecho (❌)**. Puedes subir imágenes de ejemplo:")

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

# Se pueden añadir más cortes según se necesite


