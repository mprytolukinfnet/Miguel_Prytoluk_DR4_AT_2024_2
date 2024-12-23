from src.call_llm import call_llm
import pandas as pd
import requests
import json
import time
import os
import matplotlib.pyplot as plt

URL_BASE = 'https://dadosabertos.camara.leg.br/api/v2'

def limpar_codigo(codigo):
    return codigo.replace('python', '', 1).replace('```', '')

def find_between(s, start, end):
        return s.split(start)[1].split(end)[0]

def insights_deputados():
    # Coleta de dados
    url = f"{URL_BASE}/deputados?dataInicio=2024-08-01&dataFim=2024-08-30"
    response = requests.get(url).json()
    deputados = pd.DataFrame(response['dados'])

    # Salvar em Parquet
    deputados.to_parquet('data/deputados.parquet')

    # Contagem de partidos
    party_count = deputados['siglaPartido'].value_counts()

    # Retornando o código para gerar o gráfico
    codigo_grafico = limpar_codigo(call_llm("""Crie o código em python que gere um gráfico de pizza com o total e o percentual de deputados de cada um de todos os partidos, e salve em 'docs/distribuicao_deputados.png'
    A contagem de partidos está constante na variável `party_count`, gerada como `party_count = deputados['siglaPartido'].value_counts()`
    O gráfico deve mostrar todos os partidos, com exceção dos muito pequenos que podem ser agrupados como outros, e não apenas os 4 ou 5 maiores.
    Se você criar uma função, essa função deve ser chamada no seu código, sem ser num comentário. Apenas chame a função, não gere a base de dados. Presuma que a variável party_count já tenha sido criada.
    Você deve retornar apenas o código em python a ser executado, contendo as bibliotecas a serem importadas, e mais nenhum texto."""))

    #Executando o código para gerar o gráfico
    exec(codigo_grafico)

    analise = call_llm(f"""Você é um analista político especializado no funcionamento legislativo do Brasil. Sua tarefa é analisar a seguinte distribuição de deputados por partido e gerar insights sobre como essa configuração pode influenciar a tomada de decisões na Câmara dos Deputados. Considere os efeitos de maiorias, alianças e fragmentação partidária.
    A saída da sua resposta deve ser um código JSON válido.
                   
    Aqui estão os dados da distribuição:

    {party_count}.

    Exemplos de análises que buscamos:
    1. Os partidos políticos com mais deputados na câmara são: ...
    2. Partidos com maior representação tendem a liderar a agenda legislativa e controlar as comissões mais importantes.
    3. Uma fragmentação partidária alta pode dificultar a formação de consensos e aumentar a necessidade de negociações multipartidárias.

    Agora, gere insights detalhados sobre a composição da Câmara dos Deputados, e sobre os impactos da distribuição de partidos na Câmara, considerando as dinâmicas políticas e legislativas.
    O formato desejado é:
    '''json
    [{{"analise": "insight 1"}},{{"analise": "insight 2"}}]
    '''
    Gere apenas o código JSON sem mais nenhum texto.
    """)

    deputados_json_str = find_between(analise, '```json', '```')

    with open('data/insights_distribuicao_deputados.json', 'w', encoding='utf-8') as f:
            deputados_json = json.loads(deputados_json_str)
            json.dump(deputados_json, f, ensure_ascii=False, indent=4)

def insights_despesas_deputados():
    # Caminho do arquivo Parquet
    parquet_file = 'data/despesas_deputados.parquet'
    # Verificar se o arquivo Parquet já existe
    if os.path.exists(parquet_file):
        # Se o arquivo existir, importar os dados
        despesas_agrupadas = pd.read_parquet(parquet_file)
    else:
        # Coletar dados de deputados
        url_deputados = f"{URL_BASE}/deputados?dataInicio=2024-08-01&dataFim=2024-08-30"
        response_deputados = requests.get(url_deputados).json()
        deputados = pd.DataFrame(response_deputados['dados'])

        # Coletar despesas dos deputados
        despesas_list = []
        for idx, dados_deputado in deputados.iterrows():
            deputado_id = dados_deputado['id']
            deputado_nome = dados_deputado['nome']
            url_despesas = f"{URL_BASE}/deputados/{deputado_id}/despesas"
            response_despesas = requests.get(url_despesas).json()
            for dado in response_despesas['dados']:
                dado['idDeputado'] = deputado_id
                dado['nomeDeputado'] = deputado_nome
            dados = response_despesas['dados']
            despesas_list.extend(dados)

        # Criar DataFrame com as despesas
        despesas = pd.DataFrame(despesas_list)

        # Agrupar dados por dia, deputado e tipo de despesa
        
        despesas_agrupadas = (
            despesas.groupby(['dataDocumento', 'idDeputado', 'nomeDeputado', 'tipoDespesa'])
            .agg({'valorLiquido': 'sum'})
            .reset_index()
        )

        # Salvar em arquivo Parquet
        despesas_agrupadas.to_parquet(parquet_file, index=False)

    # Prompt-Chaining: Etapa 1 - Deputados com mais despesas
    prompt_analise_1 = f"""
Você é um cientista de dados. O arquivo 'data/despesas_deputados.parquet' contém os seguintes campos:
- `dataDocumento`: Data da despesa.
- `idDeputado`: Identificador único do deputado.
- `nomeDeputado`: Nome do deputado.
- `tipoDespesa`: Tipo de despesa registrada.
- `valorLiquido`: Valor líquido da despesa.

Gere o código Python que:
1. Identifique os deputados com maiores despesas totais.
2. Salve os resultados da análise em um DataFrame chamado `despesas_por_deputado`, com as colunas "deputado" e "total_despesas".

Se você declarar uma função, você precisa chamar essa função, porque é necessário que executando o seu código a variável 'despesas_por_deputado' esteja atribuída.  

Retorne apenas o código Python, sem explicações adicionais.
    """
    codigo_analise_1 = limpar_codigo(call_llm(prompt_analise_1))
    exec(codigo_analise_1, globals())

    # Prompt-Chaining: Etapa 2 - Tipo de despesas mais presentes
    prompt_analise_2 = f"""
Você é um cientista de dados. O arquivo 'data/despesas_deputados.parquet' contém os seguintes campos:
- `dataDocumento`: Data da despesa.
- `idDeputado`: Identificador único do deputado.
- `nomeDeputado`: Nome do deputado.
- `tipoDespesa`: Tipo de despesa registrada.
- `valorLiquido`: Valor líquido da despesa.

Gere o código Python que:
1. Identifique os tipos de despesa com maiores valores no total.
2. Salve os resultados da análise em um DataFrame chamado `despesas_por_tipo`, com as colunas "tipo_despesa" e "total_despesas".

Se você declarar uma função, você precisa chamar essa função, porque é necessário que executando o seu código a variável 'despesas_por_tipo' esteja atribuída.  

Retorne apenas o código Python, sem explicações adicionais.
    """
    codigo_analise_2 = limpar_codigo(call_llm(prompt_analise_2))
    exec(codigo_analise_2, globals())

    # Prompt-Chaining: Etapa 3 - Deputados x tipo de despesa com maiores valores
    prompt_analise_3 = f"""
Você é um cientista de dados. O arquivo 'data/despesas_deputados.parquet' contém os seguintes campos:
- `dataDocumento`: Data da despesa.
- `idDeputado`: Identificador único do deputado.
- `nomeDeputado`: Nome do deputado.
- `tipoDespesa`: Tipo de despesa registrada.
- `valorLiquido`: Valor líquido da despesa.

Gere o código Python que:
1. Identifique o quanto cada Deputado gastou com cada tipo de despesa, e retorne os pares de "deputado" x "tipo_despesa" que tiverem os maiores valores de "total_despesas".
2. Salve os resultados da análise em um DataFrame chamado `despesas_por_deputado_e_tipo`, com as colunas "deputado", "tipo_despesa" e "total_despesas".

Se você declarar uma função, você precisa chamar essa função, porque é necessário que executando o seu código a variável 'despesas_por_deputado_e_tipo' esteja atribuída.  

Retorne apenas o código Python, sem explicações adicionais.
    """
    codigo_analise_3 = limpar_codigo(call_llm(prompt_analise_3))
    exec(codigo_analise_3, globals())

    global analise_maior_gasto, analise_tendencias, analise_variacao
    
    # Prompt para Insights com Generated Knowledge
    prompt_insights = f"""
Você é um analista político e econômico.
Gere insights sobre os dados de despesas dos deputados em formato JSON.
As seguintes dados foram levantados sobre os as despesas dos deputados:
1. Deputados com maiores gastos totais:
{despesas_por_deputado.to_json(orient="records", date_format="iso")}

2. Tipos de despesa com maior despesa:
{despesas_por_tipo.to_json(orient="records", date_format="iso")}

3. Deputados x Tipos de Despesa com maiores valores:
{despesas_por_deputado_e_tipo.to_json(orient="records", date_format="iso")}

Utilizando os dados providenciados, gere insights detalhados sobre:
1. Quais deputados tiveram as maiores despesas?
2. Quais tipos de despesa são os mais presentes?
3. Quais deputados estão gastando mais em quais tipos de despesa?

    O formato desejado é:
    '''json
    [{{"analise": "insight 1"}},{{"analise": "insight 2"}}]
    '''
    Gere apenas o código JSON sem mais nenhum texto.
    """
    insights = call_llm(prompt_insights)

    # Salvar insights em arquivo JSON
    despesas_json_str = find_between(insights, '```json', '```')
    with open('data/insights_despesas_deputados.json', 'w', encoding='utf-8') as f:
                despesas_json = json.loads(despesas_json_str)
                json.dump(despesas_json, f, ensure_ascii=False, indent=4)

def coleta_proposicoes():
    # Definir os códigos temáticos e inicializar lista para as proposições
    temas = {"Economia": 40, "Educação": 46, "Ciência, Tecnologia e Inovação": 62}
    proposicoes_list = []

    # Coletar dados de proposições para cada tema
    for tema, codigo in temas.items():
        url_proposicoes = (
            f"{URL_BASE}/proposicoes?dataInicio=2024-08-01&dataFim=2024-08-30&"
            f"codTema={codigo}&itens=10&ordem=ASC&ordenarPor=id"
        )
        response_proposicoes = requests.get(url_proposicoes).json()
        for proposicao in response_proposicoes.get('dados', []):
            proposicao['tema'] = tema
            proposicoes_list.append(proposicao)

    # Criar DataFrame com proposições coletadas
    proposicoes = pd.DataFrame(proposicoes_list)

    # Salvar proposições em Parquet
    proposicoes.to_parquet('data/proposicoes_deputados.parquet', index=False)

    # Prompt para sumarização
    sumarizacoes = []
    for i, proposicao in proposicoes.iterrows():
        prompt_sumarizacao = f"""
    Você é um assistente especializado em sumarização de textos legislativos. Resuma a seguinte proposição legislativa:
    {proposicao.ementa}

    Forneça uma sumarização curta e objetiva. Lembre-se de que a sumarização deve ser fiel ao texto original, mas em suas próprias palavras."""
        resumo = call_llm(prompt_sumarizacao)
        sumarizacoes.append({'tema': proposicao.tema, 'sumarizacao': resumo})
        time.sleep(4)

    # Salvar sumarização em JSON
    sumarizacoes_df = pd.DataFrame(sumarizacoes)

    # Salvar sumarizações em JSON
    sumarizacoes_df.to_json('data/sumarizacao_proposicoes.json', orient='records')
