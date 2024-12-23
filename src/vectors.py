try:
    from src.call_llm import call_llm
except ImportError:
    from call_llm import call_llm
from transformers import AutoTokenizer, AutoModel
import faiss
import torch
import pandas as pd
import json
import numpy as np

# Inicialização do modelo de embeddings
model = AutoModel.from_pretrained('neuralmind/bert-base-portuguese-cased')
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)

# Função para criar base vetorial FAISS
def criar_base_vetorial():
    # Verificar se GPU está disponível
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Carregar dados
    with open("data/insights_distribuicao_deputados.json", "r", encoding="utf-8") as f:
        insights_distribuicao_deputados = json.load(f)
    with open("data/insights_despesas_deputados.json", "r", encoding="utf-8") as f:
        insights_despesas_deputados = json.load(f)
    with open("data/sumarizacao_proposicoes.json", "r", encoding="utf-8") as f:
        proposicoes_resumo = json.load(f)
    
    # Unificar os dados em texto para vetorizar
    textos = []

    # Lista de deputados por partido
    # Deputados
    for insight in insights_distribuicao_deputados:
        textos.append(insight['analise'])

    # Despesas
    for insight in insights_despesas_deputados:
        textos.append(insight['analise'])

    # Proposições
    for proposicao in proposicoes_resumo:
        textos.append(f"Tema: {proposicao['tema']}. Proposição: {proposicao['sumarizacao']}")

    # Parâmetros
    batch_size = 128
    embeddings = []

    print(f'Número de textos: {len(textos)}')
    # Processamento em mini-batches
    for i in range(0, len(textos), batch_size):
        print(f"Batch:{i}-{min(i+batch_size, len(textos))}")
        # Criar lote
        mini_batch = textos[i:i + batch_size]
        
        # Tokenizar o mini-batch
        tokens = tokenizer(mini_batch, padding=True, truncation=True, return_tensors="pt")
        tokens = {key: value.to(device) for key, value in tokens.items()}

        
        # Gerar embeddings
        with torch.no_grad():
            outputs = model(**tokens)
            hidden_states = outputs.last_hidden_state
            mini_batch_embeddings = hidden_states.mean(dim=1)  # Mean pooling
        
        # Converter para CPU e adicionar aos resultados finais
        embeddings.append(mini_batch_embeddings.cpu().numpy())

    # Concatenar todos os embeddings
    embeddings = np.vstack(embeddings)
    # Normalizar os embeddings
    faiss.normalize_L2(embeddings)


    # Criar índice FAISS
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embeddings)
    faiss.write_index(index, "data/faiss_index.bin")

    # Salvar textos associados
    with open("data/textos_faiss.json", "w", encoding="utf-8") as f:
        json.dump(textos, f, ensure_ascii=False, indent=4)

# Interface com o assistente virtual
def chat_assistente(prompt_usuario):
    # Carregar índice e textos
    index = faiss.read_index("data/faiss_index.bin")
    with open("data/textos_faiss.json", "r", encoding="utf-8") as f:
        textos = json.load(f)
    
    # Gerar embedding do prompt
    tokens = tokenizer(prompt_usuario, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**tokens)
        query_embedding = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
        # Normalizar o embedding da consulta
        faiss.normalize_L2(query_embedding)

    
    # Pesquisar no índice FAISS os k vetores semelhantes
    _, indices = index.search(query_embedding, k=128)

    # Recuperar textos relevantes
    respostas_relevantes = [textos[i] for i in indices[0]]

    # print(respostas_relevantes)
    
    # Técnica Self-Ask
    prompt_self_ask = f"""
    Você é um assistente virtual especializado em Câmara dos Deputados.
    Responda com base nas seguintes informações:
    {respostas_relevantes}
    
    Pergunta do usuário: {prompt_usuario}.
    Se necessário, crie subperguntas para encontrar a resposta e responda de forma clara e objetiva.
    Por exemplo, perguntas complexas, como "Qual deputado teve o maior gasto em Educação no último mês?", podem ser decompostas em:
    - Quais deputados têm gastos em Educação?
    - Qual foi o maior gasto registrado no último mês?
    - Quem realizou esse gasto?
    """
    resposta = call_llm(prompt_self_ask)
    return resposta
