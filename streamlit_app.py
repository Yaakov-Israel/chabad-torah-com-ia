import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
import google.generativeai as genai # SDK direta do Google também é necessária para configurar a chave

# --- Configuração da Página Streamlit ---
st.set_page_config(page_title="Gaon da IA - Super Agente PME", layout="wide", initial_sidebar_state="expanded")

# --- Carregar API Key e Configurar Modelo ---
# Esta é a forma correta de carregar a API Key no Streamlit Cloud
# Você precisará configurar um "Secret" no Streamlit Cloud chamado GOOGLE_API_KEY
GOOGLE_API_KEY = None
llm = None # Inicializa llm como None

try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError: # Chave não encontrada nos secrets do Streamlit
    st.error("🚨 ERRO: Chave API 'GOOGLE_API_KEY' não encontrada nos Segredos (Secrets) do Streamlit.")
    st.info("Por favor, adicione sua GOOGLE_API_KEY aos Segredos do seu aplicativo no painel do Streamlit Community Cloud.")
    st.stop() # Interrompe a execução se a chave não for encontrada
except FileNotFoundError: # Para desenvolvimento local se o .streamlit/secrets.toml não existir
    st.error("🚨 ERRO: Arquivo de Segredos (secrets.toml) não encontrado para desenvolvimento local.")
    st.info("Crie um arquivo .streamlit/secrets.toml com sua GOOGLE_API_KEY ou configure-a nos Segredos do Streamlit Cloud.")
    st.stop()


if not GOOGLE_API_
