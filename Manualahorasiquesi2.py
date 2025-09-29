import os
import streamlit as st
from docx import Document
from PIL import Image

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Manual Operador Super10", page_icon="🛒", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    body {
        background-color: #fdfdfd;
        color: #333333;
    }
    .seccion {
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        background-color: #fff8e1; /* amarillo claro */
        border-left: 6px solid #f39c12; /* naranjo corporativo */
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
    }
    .titulo-seccion {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #f39c12; /* naranjo */
    }
    .subtitulo {
        font-size: 20px;
        font-weight: 600;
        margin-top: 1rem;
        color: #e67e22; /* naranjo un poco más oscuro */
    }
    .correcto {
        background-color: #eafaf1;
        padding: 0.5rem;
        border-radius: 8px;
        color: #27ae60;
        font-weight: 600;
        border-left: 4px solid #27ae60;
        margin-top: 0.5rem;
    }
    .incorrecto {
        background-color: #fdecea;
        padding: 0.5rem;
        border-radius: 8px;
        color: #c0392b;
        font-weight: 600;
        border-left: 4px solid #c0392b;
        margin-top: 0.5rem;
    }
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, #f39c12, #f1c40f);
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- TÍTULO ---
st.title("📘 Manual Operador Sala / Super10")
st.markdown("Versión digital **corporativa** con colores naranjo y amarillo.")

# --- CARGAR DOCX ---
doc_path = os.path.join(os.path.dirname(__file__), "manual_operador_sala_super10_checklist.docx")
doc = Document(doc_path)

# --- ICONOS / IMÁGENES ---
ICONOS = {
    "caja": "caja.png",
    "sala": "sala.png",
    "carnicería": "carniceria.png"
}

# --- FUNCIÓN PARA BLOQUES ---
def render_bloque(titulo, contenido, allow_upload=False):
    st.markdown(f"<div class='subtitulo'>{titulo}</div>", unsafe_allow_html=True)
    for linea in contenido:
        if linea.startswith("✅"):
            st.markdown(f"<div class='correcto'>{linea}</div>", unsafe_allow_html=True)
            if allow_upload:
                ok_file = st.file_uploader(f"Sube ejemplo CORRECTO para {titulo}", type=["jpg","png"], key=f"ok_{titulo}")
                if ok_file:
                    st.image(Image.open(ok_file), caption=f"✅ Correcto en {titulo}", use_column_width=True)
        elif linea.startswith("❌"):
            st.markdown(f"<div class='incorrecto'>{linea}</div>", unsafe_allow_html=True)
            if allow_upload:
                bad_file = st.file_uploader(f"Sube ejemplo INCORRECTO para {titulo}", type=["jpg","png"], key=f"bad_{titulo}")
                if bad_file:
                    st.image(Image.open(bad_file), caption=f"❌ Incorrecto en {titulo}", use_column_width=True)
        else:
            st.write(linea)

# --- ESTRUCTURA ---
ESTRUCTURA = {
    "Caja": ["Impresora en caja", "Pagos"],
    "Sala": ["Mermas", "Códigos de mermas", "Cómo reponer"],
    "Carnicería": ["Equipos", "Tipos de cortes"]
}

secciones = {}
seccion_actual = None
subseccion_actual = None

for p in doc.paragraphs:
    text = p.text.strip()
    if not text:
        continue
    t_lower = text.lower()
    for gsec, subsecs in ESTRUCTURA.items():
        if t_lower.startswith(gsec.lower()):
            seccion_actual = gsec
            subseccion_actual = None
            secciones[seccion_actual] = {}
            continue
    if seccion_actual:
        for sub in ESTRUCTURA.get(seccion_actual, []):
            if t_lower.startswith(sub.lower()):
                subseccion_actual = sub
                secciones[seccion_actual][subseccion_actual] = []
                break
        else:
            if subseccion_actual:
                secciones[seccion_actual][subseccion_actual].append(text)

# --- RENDERIZAR ---
for gsec, subsecs in secciones.items():
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 6])
    with col1:
        icon_path = ICONOS.get(gsec.lower())
        if icon_path and os.path.exists(os.path.join(os.path.dirname(__file__), icon_path)):
            st.image(os.path.join(os.path.dirname(__file__), icon_path), width=80)
        else:
            st.write("📌")
    with col2:
        st.markdown(f"<div class='titulo-seccion'>{gsec}</div>", unsafe_allow_html=True)

    for ssec, contenido in subsecs.items():
        allow_upload = "reponer" in ssec.lower() or "cortes" in ssec.lower()
        with st.container():
            st.markdown("<div class='seccion'>", unsafe_allow_html=True)
            render_bloque(ssec, contenido, allow_upload=allow_upload)
            st.markdown("</div>", unsafe_allow_html=True)

# --- TIPOS DE CORTES ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='titulo-seccion'>🔪 Tipos de cortes (Ejemplo práctico)</div>", unsafe_allow_html=True)

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



