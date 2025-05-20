import streamlit as st

st.set_page_config(page_title="CHABAD - Torá com IA", layout="wide")

st.title("🌟 CHABAD - Torá com IA 🌟")
st.subheader("Seu Assistente Interativo para Estudo da Torá e Judaísmo")
# streamlit_app.py (continuação)

import google.generativeai as genai
import streamlit as st # streamlit já deve estar importado, mas só para garantir

# Carregar a API Key dos Segredos do Streamlit
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError: # Chave não encontrada nos segredos
    st.error("Chave API 'GOOGLE_API_KEY' não encontrada nos Segredos do Streamlit.")
    st.caption("Adicione sua chave API do Google Gemini aos segredos do seu app no Streamlit Cloud.")
    st.stop() # Impede a execução se a chave não estiver lá
except FileNotFoundError: # Arquivo secrets.toml não encontrado (mais para local)
    st.error("Arquivo de Segredos do Streamlit (secrets.toml) não encontrado.")
    st.caption("Configure a GOOGLE_API_KEY corretamente.")
    st.stop()

if not GOOGLE_API_KEY: # Verificação adicional
    st.error("A GOOGLE_API_KEY foi carregada, mas está vazia. Verifique os segredos.")
    st.stop()

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # st.sidebar.success("API Key configurada!") # Feedback visual opcional na barra lateral
except Exception as e_apikey_config:
    st.sidebar.error(f"Erro ao configurar a API Key do Gemini: {e_apikey_config}")
    st.stop()

# Inicializar o modelo de IA (faça UMA VEZ no início do script)
try:
    modelo_ia_principal = genai.GenerativeModel('gemini-1.5-flash-latest')
    # st.sidebar.info("Modelo Gemini carregado.") # Feedback opcional
except Exception as e_model_load:
    st.sidebar.error(f"Erro ao carregar o modelo Gemini ('gemini-1.5-flash-latest'): {e_model_load}")
    st.caption("Verifique o nome do modelo e se sua API key tem permissão.")
    st.stop()

# O resto do seu código da interface (st.title, etc.) continua abaixo...
st.write("Bem-vindo! Este é o início do nosso aplicativo.")
st.balloons() # Só para ter um efeito visual de que funcionou!
