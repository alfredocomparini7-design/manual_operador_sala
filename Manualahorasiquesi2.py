import os
import streamlit as st

# --- CONFIGURACIÓN PÁGINA ---
st.set_page_config(page_title="Manual Operador Super10", page_icon="🛒", layout="wide")

# --- ESTILOS CORPORATIVOS (AMARILLO Y ANARANJADO) ---
st.markdown("""
    <style>
    body {
        background-color: #fff8e1;
        color: #333333;
    }
    .seccion {
        padding: 1.2rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
        background: linear-gradient(90deg, #ffe082 0%, #ffcc80 100%);
        box-shadow: 0px 2px 8px rgba(255, 193, 7, 0.08);
    }
    .titulo-seccion {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 0.7rem;
        color: #ff9800;
        letter-spacing: 1px;
    }
    .subtitulo {
        font-size: 22px;
        font-weight: 700;
        margin-top: 1.1rem;
        color: #f57c00;
    }
    .correcto {
        background-color: #fffde7;
        padding: 0.6rem;
        border-radius: 8px;
        color: #fbc02d;
        font-weight: 700;
    }
    .incorrecto {
        background-color: #ffebee;
        padding: 0.6rem;
        border-radius: 8px;
        color: #e65100;
        font-weight: 700;
    }
    hr {
        border: none;
        border-top: 2px solid #ffb300;
        margin: 2rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITULO APP ---
st.title("📘 Manual Operador Sala / Super10")
st.markdown("Versión digital corporativa con **secciones visuales, íconos y ejemplos**.")

# --- ICONOS / IMÁGENES ---
ICONOS = {
    "caja": "caja.png",
    "sala": "sala.png",
    "carnicería": "carniceria.png"
}

# --- LEER Y MOSTRAR EL MANUAL ORGANIZADO ---
md_path = os.path.join(os.path.dirname(__file__), "manual_organizado.md")
with open(md_path, "r", encoding="utf-8") as f:
    manual_md = f.read()

# --- RENDER VISUAL CON ICONOS ---
import re

def render_manual_with_icons(md_text):
    # Insertar iconos antes de las secciones principales
    icon_map = {
        "CAJA": ICONOS.get("caja", ""),
        "Sala / Bodega / Reponedor (Sistema 4x1)": ICONOS.get("sala", ""),
        "Carnicería": ICONOS.get("carnicería", "")
    }
    # Separar por secciones principales
    secciones = re.split(r'(^## .+)', md_text, flags=re.MULTILINE)
    for i, sec in enumerate(secciones):
        if sec.startswith('## '):
            sec_name = sec[3:].strip()
            icon_path = icon_map.get(sec_name)
            if icon_path and os.path.exists(os.path.join(os.path.dirname(__file__), icon_path)):
                img_html = f'<img src="file://{os.path.join(os.path.dirname(__file__), icon_path)}" width="60" style="vertical-align:middle; margin-right:10px;">'
            else:
                img_html = '🟧'
            secciones[i] = f'<div class="titulo-seccion">{img_html}{sec_name}</div>'
    # Unir y mostrar
    html_content = ''.join(secciones)
    # Convertir subtítulos
    html_content = re.sub(r'### (.+)', r'<div class="subtitulo">\1</div>', html_content)
    # Convertir bloques correctos/incorrectos
    html_content = re.sub(r'(✅ .+)', r'<div class="correcto">\1</div>', html_content)
    html_content = re.sub(r'(❌ .+)', r'<div class="incorrecto">\1</div>', html_content)
    # Convertir bloques de sección
    html_content = re.sub(r'(\n\n)', r'<div class="seccion"></div>', html_content)
    st.markdown(html_content, unsafe_allow_html=True)

render_manual_with_icons(manual_md)






