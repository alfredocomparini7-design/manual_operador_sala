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
st.markdown("Versión digital  ** Ojalas les sirva**.")

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


def get_icon_for_text(text):
    """Devuelve el HTML de un ícono o imagen según la palabra clave en el texto."""
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
        ("corredora", None, ""),
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

def render_manual_with_icons(md_text):
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

       

