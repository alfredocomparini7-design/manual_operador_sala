import os
import streamlit as st
import re
import io
from PIL import Image

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
        padding: 0;
        border-radius: 0;
        margin-bottom: 0;
        background: none;
        box-shadow: none;
    }
    .titulo-seccion {
        font-size: 28px;
        font-weight: 800;
        margin-bottom: 0.7rem;
        color: #ff9800;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #ffe082 0%, #ffcc80 100%);
        border-radius: 14px;
        padding: 1.2rem;
        box-shadow: 0px 2px 8px rgba(255, 193, 7, 0.08);
    }
    .subtitulo {
        font-size: 22px;
        font-weight: 700;
        margin-top: 1.1rem;
        color: #f57c00;
        background: linear-gradient(90deg, #fffde7 0%, #ffe0b2 100%);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        box-shadow: 0px 1px 4px rgba(255, 193, 7, 0.06);
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

def get_icon_for_text(text):
    """Devuelve el HTML de un ícono o imagen según la palabra clave en el texto, excepto para 'corredora'."""
    iconos_palabras = [
        ("caja", ICONOS.get("caja", ""), "🟧"),
        ("sala", ICONOS.get("sala", ""), "🟦"),
        ("carnicería", ICONOS.get("carnicería", ""), "🥩"),
        ("mermas", None, "♻️"),
        ("pagos", None, "💳"),
        ("impresora", None, "🖨️"),
        ("equipos", None, "⚙️"),
        ("reponer", None, "🛒"),
        ("factura", None, "📄"),
        ("aluzado", None, "🌀"),
        # ("corredora", None, "🚚"),  # Removido el ícono para corredora
        ("glosario", None, "📖")
    ]
    text_lower = text.lower()
    for palabra, img, emoji in iconos_palabras:
        if palabra in text_lower:
            if img and os.path.exists(os.path.join(os.path.dirname(__file__), img)):
                return f'<img src="file://{os.path.join(os.path.dirname(__file__), img)}" width="38" style="vertical-align:middle; margin-right:8px;">'
            else:
                return f'<span style="font-size:1.6em; vertical-align:middle; margin-right:8px;">{emoji}</span>'
    return ''

def render_images_from_markdown(md_text):
    """Detecta imágenes en markdown y las muestra con st.image, devolviendo el markdown sin esas imágenes."""
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = list(re.finditer(img_pattern, md_text))
    last_idx = 0
    cleaned_md = ""
    for match in matches:
        start, end = match.span()
        alt_text, img_path = match.groups()
        cleaned_md += md_text[last_idx:start]
        # Mostrar la imagen si existe
        img_abspath = os.path.join(os.path.dirname(__file__), img_path)
        if os.path.exists(img_abspath):
            st.image(img_abspath, caption=alt_text, use_column_width=True)
        else:
            cleaned_md += f"[Imagen no encontrada: {alt_text}]"
        last_idx = end
    cleaned_md += md_text[last_idx:]
    return cleaned_md

def render_manual_with_icons(md_text):
    # Primero, mostrar imágenes y limpiar el markdown
    md_text = render_images_from_markdown(md_text)
    # Separar por secciones principales
    secciones = re.split(r'(^## .+)', md_text, flags=re.MULTILINE)
    for i, sec in enumerate(secciones):
        if sec.startswith('## '):
            sec_name = sec[3:].strip()
            icon_html = get_icon_for_text(sec_name)
            secciones[i] = f'<div class="titulo-seccion">{icon_html}{sec_name}</div>'
    # Unir y buscar subsecciones
    html_content = ''.join(secciones)
    # Subtítulos con íconos
    def subtitulo_replacer(match):
        subtitulo = match.group(1)
        icon_html = get_icon_for_text(subtitulo)
        return f'<div class="subtitulo">{icon_html}{subtitulo}</div>'
    html_content = re.sub(r'### (.+)', subtitulo_replacer, html_content)
    # Convertir bloques correctos/incorrectos
    html_content = re.sub(r'(✅ .+)', r'<div class="correcto">\1</div>', html_content)
    html_content = re.sub(r'(❌ .+)', r'<div class="incorrecto">\1</div>', html_content)
    # Convertir bloques de sección
    html_content = re.sub(r'(\n\n)', r'<div class="seccion"></div>', html_content)
    st.markdown(html_content, unsafe_allow_html=True)

render_manual_with_icons(manual_md)
