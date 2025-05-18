import streamlit as st
from PIL import Image
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Configuração inicial
st.set_page_config(page_title="Dra. Lima - Alimentação na Gravidez", layout="centered")

from PIL import Image

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    logo = Image.open("assets/Logo.png")
    st.image(logo, width=200)

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.0-flash")

# Estado de exibição
if "etapa" not in st.session_state:
    st.session_state.etapa = "inicio"  # ou "resultado"

st.title("🤰 O que posso comer, Dra. Luma?")
st.markdown("Envie uma foto de um alimento ou embalagem para saber se é indicado durante a gravidez.")

# ETAPA 1 - Envio da imagem
if st.session_state.etapa == "inicio":
    imagem = st.file_uploader("📸 Envie a imagem aqui", type=["jpg", "jpeg", "png"])

    if imagem:
        st.image(imagem, caption="Imagem enviada", use_container_width=True)
        with st.spinner("Analisando com carinho..."):
            try:
                image = Image.open(imagem)
                prompt = """
Você é uma nutricionista especializada em gestantes. Com base na imagem, identifique os alimentos e diga para cada um:

1. Se pode ou não na gravidez.
2. Calorias por 100g ou 100ml.
3. Um benefício para a gestação, se houver.

Responda de forma curta, clara e acolhedora. Se não for possível identificar alimentos, diga isso com carinho.
"""
                resposta = model.generate_content([prompt, image])
                st.session_state.resultado = resposta.text
                st.session_state.etapa = "resultado"
                st.rerun()

            except Exception as e:
                st.error(f"Ocorreu um erro na análise: {e}")

# ETAPA 2 - Exibição do resultado
elif st.session_state.etapa == "resultado":
    st.success("Análise concluída!")
    st.markdown(st.session_state.resultado)

    if st.button("🔄 Analisar outro alimento"):
        st.session_state.etapa = "inicio"
        st.session_state.resultado = ""
        st.rerun()
