from src.call_llm import call_llm
import os

def limpar_codigo(codigo):
    return codigo.replace('python', '', 1).replace('```', '')

# Função para executar o processo de Chain-of-Thought prompting
def gerar_dashboard_chain_of_thought():
    # Prompt 1: Estrutura inicial e abas
    prompt_estrutura = """
Você é um desenvolvedor experiente. O dashboard terá 3 abas: Overview, Despesas e Proposições.
Escreva o código inicial em Python usando Streamlit para criar essas abas. Não adicione conteúdo ainda.
O código deve definir as abas e o layout do aplicativo.
Certifique-se de que o título da aplicação (st.title) é "Análise da Câmara de Deputados"
    """
    codigo_estrutura = limpar_codigo(call_llm(prompt_estrutura))

    # Prompt 2: Conteúdo da aba Overview, utilizando a estrutura inicial
    prompt_overview = f"""
Agora, implemente a aba Overview do dashboard criado no código abaixo:
{codigo_estrutura}

A aba Overview deve conter:
- Um título e descrição geral da solução - O título deve ser ("Visão Geral") e a descrição da aba Overview deve deixar claro que se trata de um dashboard que analisa dados da Câmara de Deputados de Agosto/2024.
- Um gráfico de pizza (carregar de `docs/distribuicao_deputados.png`).
- Insights sobre a distribuição de deputados (carregar de `data/insights_distribuicao_deputados.json`) na estrutura [{{"analise": "insight 1"}},{{"analise": "insight 2"}}].

Para a imagem não utilize o parâmetro depreciado "use_column_width", utilize "use_container_width" no lugar.

Forneça apenas o código necessário para completar a aba Overview no dashboard, integrando à estrutura existente.
    """
    codigo_overview = limpar_codigo(call_llm(prompt_overview))

    # Prompt 3: Combinação do código final
    prompt_final = f"""
Combine o seguinte código em um único arquivo funcional para o dashboard:
1. Estrutura inicial com abas:
{codigo_estrutura}

2. Implementação da aba Overview:
{codigo_overview}

Certifique-se de que o código final seja executável, com boas práticas e sem redundâncias.
Você deve importar todas as bibliotecas que forem utilizadas no código, inclusive a biblioteca para mostara a imagem. Não esqueça de nenhuma importação.
Retorne apenas o código em python final completo, não retorne nenhum texto extra que impeça a execução do arquivo.
    """
    dashboard_code = limpar_codigo(call_llm(prompt_final))

    # Salvar o código final em um arquivo Python
    with open("src/dashboard.py", "w", encoding="utf-8") as f:
        f.write(dashboard_code)

def gerar_dashboard_completo():
    # Verificar se o arquivo base existe
    dashboard_path = "src/dashboard.py"
    if not os.path.exists(dashboard_path):
        raise FileNotFoundError(f"O arquivo {dashboard_path} não foi encontrado. Certifique-se de que ele exista antes de continuar.")

    # Ler o código atual do dashboard
    with open(dashboard_path, "r", encoding="utf-8") as f:
        codigo_atual = f.read()

    # Prompt único para Batch-prompting
    prompt_batch = f"""
Você é um desenvolvedor especializado em Streamlit. O seguinte código é um dashboard já funcional:
{codigo_atual}

Agora, adicione duas novas abas ao dashboard: "Despesas" e "Proposições". Cada aba deve incluir os seguintes elementos:

1. **Aba Despesas**:
   - Carregue os insights das despesas de `data/insights_despesas_deputados.json` e exiba-os no painel. O arquivo tem a estrutura [{{"analise": "insight 1"}},{{"analise": "insight 2"}}].
   - Adicione um `st.selectbox` para selecionar um deputado pelo nome.
   - Mostre um gráfico de barras com a série temporal de despesas do deputado selecionado (dados de `data/despesas_deputados.parquet`, com as colunas "dataDocumento", "idDeputado", "nomeDeputado", "tipoDespesa" e "valorLiquido").

2. **Aba Proposições**:
   - Carregue e exiba os dados das proposições de `data/proposicoes_deputados.parquet` em uma tabela.
   - Mostre o resumo das proposições a partir do arquivo `data/sumarizacao_proposicoes.json`, que está na estrutura [{{"tema": "Educação","sumarizacao": "Resumo_1"}}, {{"tema": "Economia","sumarizacao": "Resumo_2"}}].

   Certifique-se de que o código final seja executável, com boas práticas e sem redundâncias.
    Retorne apenas o código em python final completo do arquivo dashboard.py, não retorne nenhum texto extra que impeça a execução do arquivo.
    """
    # Chamada ao LLM
    dashboard_completo = limpar_codigo(call_llm(prompt_batch))

    # Salvar o código atualizado no arquivo dashboard.py
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_completo)

    print("Arquivo 'dashboard.py' atualizado com sucesso!")
