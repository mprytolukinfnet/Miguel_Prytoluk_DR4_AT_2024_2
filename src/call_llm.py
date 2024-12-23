import google.generativeai as genai

import os
from dotenv import load_dotenv
from pathlib import Path

# Carregas as variáveis de ambiente
load_dotenv(dotenv_path=Path("../.env"))
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configuração da API Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Função para chamar a API Gemini
def call_llm(prompt_text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt_text)
    return response.text
