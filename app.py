import streamlit as st
import requests
import os
from gtts import gTTS
import base64

# Configurações de Segurança e API
HF_TOKEN = st.secrets["HF_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

def consultar_ia(texto):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    prompt = f"<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nVocê é um médico didático. Explique termos médicos de forma simples para leigos.<|eot_id|><|start_header_id|>user<|end_header_id|>\n\nExplique: {texto}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}})
        return response.json()[0]['generated_text'].split("assistant")[-1].strip()
    except:
        return "IA carregando... Tente novamente em instantes."

# Interface do Usuário
st.set_page_config(page_title="Doutor Explica", page_icon="⚕️")
st.title("⚕️ Doutor Explica")
st.write("Traduza laudos médicos para linguagem simples gratuitamente.")

entrada = st.text_area("Cole seu exame aqui:", height=150)

if st.button("Simplificar Agora"):
    if entrada:
        with st.spinner("Analisando..."):
            resultado = consultar_ia(entrada)
            st.subheader("Explicação:")
            st.write(resultado)
            
            # Opção de Áudio
            tts = gTTS(text=resultado, lang='pt-br')
            tts.save("audio.mp3")
            st.audio("audio.mp3")
            
            # Opção de PDF
            st.download_button("Baixar PDF", data=resultado, file_name="laudo.txt") # TXT por simplicidade inicial
    else:
        st.warning("Por favor, insira um texto.")

st.info("Atenção: Este app não substitui a consulta médica.")