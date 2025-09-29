import os
import streamlit as st
import re
import io
from PIL import Image

import pdfkit
import markdown2

# --- CONFIGURACIÓN PÁGINA ---
st.set_page_config(page_title="Manual Operador Super10", page_icon="🛒", layout="wide")

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

# --- BOTÓN PARA EXPORTAR A PDF ---
def exportar_pdf(md_text):
    html = markdown2.markdown(md_text)
    # Opcional: agregar estilos básicos para el PDF
    estilo = '''<style>body { font-family: Arial, sans-serif; font-size: 13px; } h1,h2,h3 { color: #ff9800; } strong { color: #d35400; }</style>'''
    html = f"""<html><head>{estilo}</head><body>{html}</body></html>"""
    # Generar PDF en memoria
    pdf_bytes = None
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            pdfkit.from_string(html, tmp_pdf.name)
            tmp_pdf.seek(0)
            pdf_bytes = tmp_pdf.read()
        os.unlink(tmp_pdf.name)
    except Exception as e:
        st.error(f"Error al generar PDF: {e}")
        return None
    return pdf_bytes

st.markdown("---")
st.subheader("Descargar manual en PDF para WhatsApp")
if st.button("📄 Descargar PDF del manual"):
    pdf_bytes = exportar_pdf(manual_md)
    if pdf_bytes:
        st.download_button(
            label="Descargar Manual Operador Super10.pdf",
            data=pdf_bytes,
            file_name="Manual_Operador_Super10.pdf",
            mime="application/pdf"
        )
    else:
        st.error("No se pudo generar el PDF.")

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
                return ("image", os.path.join(os.path.dirname(__file__), img))
            else:
                return ("emoji", emoji)
    return None

def render_images_in_flow(md_text):
    """Reemplaza la sintaxis de imagen markdown por el renderizado de la imagen en el lugar correcto."""
    img_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    parts = []
    last_idx = 0
    for match in re.finditer(img_pattern, md_text):
        start, end = match.span()
        alt_text, img_path = match.groups()
        # Agregar texto antes de la imagen
        if start > last_idx:
            parts.append(("text", md_text[last_idx:start]))
        # Agregar la imagen
        img_abspath = os.path.join(os.path.dirname(__file__), img_path)
        parts.append(("image", img_abspath, alt_text))
        last_idx = end
    # Agregar el resto del texto
    if last_idx < len(md_text):
        parts.append(("text", md_text[last_idx:]))
    return parts




def render_manual_with_icons(md_text):
    # Palabras clave a resaltar automáticamente en negrita
    palabras_negrita = [
        "Importante", "RECORDAR", "Nota", "Siempre", "Nunca", "Prohibido", "Atención", "Cuidado", "Sugerencia", "Ejemplo", "Restricciones", "Usuario", "Clave", "Local", "Configuración", "Seguridad",
        "Pistola de radiofrecuencia", "Transpaleta manual", "Transpaleta eléctrica", "Transpaleta electrica",
        "Checkout", "Barrido de sala/caja", "Cabecera", "Brecha visible", "Brecha invisible", "FEFO", "Fleje", "Flejera", "Góndola", "Isla", "Isla de congelados", "Layout", "Quiebre de stock"
    ]
    # Procesar imágenes en el flujo correcto
    parts = render_images_in_flow(md_text)
    for part in parts:
        if part[0] == "text":
            text = part[1]
            palabras_negrita_ordenadas = sorted(palabras_negrita, key=len, reverse=True)
            def bold_phrases_outside_blocks(texto, frases):
                pattern = r'(\*\*[^*]+\*\*)'
                partes = re.split(pattern, texto)
                for i, parte in enumerate(partes):
                    if not parte.startswith('**'):
                        for frase in frases:
                            def no_dup_bold(m):
                                return f'**{m.group(1)}**' if not m.group(0).startswith('**') else m.group(0)
                            if ' ' in frase:
                                pattern_frase = rf'(?<!\*)({re.escape(frase)})(?!\*)'
                            else:
                                pattern_frase = rf'(?<!\*)\b({re.escape(frase)})\b(?!\*)'
                            parte = re.sub(pattern_frase, no_dup_bold, parte)
                    partes[i] = parte
                return ''.join(partes)
            text = bold_phrases_outside_blocks(text, palabras_negrita_ordenadas)

            # Procesar por líneas para detectar títulos, subtítulos, etc.
            lines = text.split('\n')
            for line in lines:
                line_strip = line.strip()
                if line_strip.startswith('## '):
                    sec_name = line_strip[3:].strip()
                    icon = get_icon_for_text(sec_name)
                    if icon:
                        if icon[0] == "image":
                            st.image(icon[1], width=38)
                            st.header(sec_name)
                        elif icon[0] == "emoji":
                            st.header(f"{icon[1]} {sec_name}")
                        else:
                            st.header(sec_name)
                    else:
                        st.header(sec_name)
                elif line_strip.startswith('### '):
                    sub_name = line_strip[4:].strip()
                    icon = get_icon_for_text(sub_name)
                    if icon:
                        if icon[0] == "image":
                            st.image(icon[1], width=28)
                            st.subheader(sub_name)
                        elif icon[0] == "emoji":
                            st.subheader(f"{icon[1]} {sub_name}")
                        else:
                            st.subheader(sub_name)
                    else:
                        st.subheader(sub_name)
                elif line_strip.startswith('✅ '):
                    st.success(line_strip[2:].strip())
                elif line_strip.startswith('❌ '):
                    st.error(line_strip[2:].strip())
                elif line_strip == '':
                    st.write("")
                else:
                    st.markdown(line)
        elif part[0] == "image":
            img_abspath, alt_text = part[1], part[2]
            if os.path.exists(img_abspath):
                st.image(img_abspath, caption=alt_text, use_column_width=True)
            else:
                st.warning(f"[Imagen no encontrada: {alt_text}]")

render_manual_with_icons(manual_md)
