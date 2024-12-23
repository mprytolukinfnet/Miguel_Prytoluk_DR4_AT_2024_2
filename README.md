**Assessment (AT)**

**Disciplina:** Engenharia de Prompts para Ciência de Dados

**Aluno:** Miguel Belardinelli Prytoluk

**Data:** 22/12/2024


## Descrição do Projeto
**Análise da Câmara de Deputados** é uma aplicação que utiliza LLMs e um dashboard streamlit para analisar dados da Câmara dos Deputados.

## Objetivo
O objetivo principal da aplicação é facilitar a análise e interpretação de dados de dados da Câmara dos Deputados:

1. **Distribuição dos Deputados**: Análises sobre a distribuição dos deputados nos partidos.
2. **Despesas**: Análises sobre as Despesas dos Deputados na Câmara.
3. **Proposições**: Resumos das proposições no período analisado
4. **Assistente Virtual**: Chat com um Assistente Virtual para responder perguntas sobre a Câmara dos Deputados

## Diagrama da aplicação

![Diagrama da Aplicação](docs/diagrama_aplicacao.jpg?raw=true "Diagrama")

## Requisitos

- Python 3.10 ou superior
- `virtualenv` para criação de ambiente virtual
- Os pacotes listados no arquivo `requirements.txt`
- Uma chave de API Gemini

## Instruções para configurar o ambiente

### 1. Clonar o Repositório

Clone este repositório na sua máquina local.

```bash
git clone https://github.com/mprytolukinfnet/Miguel_Prytoluk_DR4_AT_2024_2.git
```

### 2. Criar um Ambiente Virtual

No diretório do projeto, crie um ambiente virtual usando `virtualenv`:

```bash
virtualenv venv
```

### 3. Ativar o Ambiente Virtual
- No Windows:
```bash
venv\Scripts\activate
```

- No Linux/Mac:
```bash
source venv/bin/activate
```

### 4. Instalar as Dependências

Com o ambiente virtual ativado, instale as dependências do projeto:
```bash
pip install -r requirements.txt
```

### Instalar Pytorch
https://pytorch.org/get-started/locally/

### Instalar biblioteca FAISS de acordo com o hardware
- **CPU**
```bash
pip install faiss-cpu==1.9.0.post1
```
- **GPU CUDA11**
```bash
pip install faiss-gpu-cu11==1.9.0.post1
```
- **GPU CUDA12**
```bash
pip install faiss-gpu-cu12==1.9.0.post1
```

### 5. Variáveis de ambiente

Criar um arquivo `.env` na raiz do projeto contendo sua chave de API Open AI no formato:
```env
GEMINI_API_KEY=chave-gemini
```

## Instruções para rodar o projeto

### Geração dos arquivos do projeto
A execução dos códigos do projeto se deram no notebook `exercicios.ipynb`. É possível acompanhar os resultados das execuções, bem como a solução dos exercícios.

### Execução do notebook
É possível ver a solução dos exercícios no arquivo `exercicios.pdf`

### Aplicação Streamlit
Para rodar a aplicação streamlit, execute o seguinte comando no terminal:
```bash
streamlit run src/dashboard.py
```

## Estrutura do Projeto

### Execução dos exercícios
- **exercicios.ipynb** -> Notebook com a execução dos códigos do projeto
- **exercicios.pdf** -> Arquivo pdf com a execução dos códigos do projeto exportada

### diretório src (código)
- **src/call_llm.py** -> código para fazer chamadas ao modelo gemini-1.5-flash
- **src/dashboard.py** -> aplicação streamlit gerada pelo modelo gemini-1.5-flash para visualização dos dados da câmara de deputados
- **src/dataprep.py** -> script de coleta e preparação dos dos dados da API do legislativo
- **src/generate_dashboard.py** -> script para executar a geração do código do arquivo src/dashboard.py pelo modelo gemini-1.5-flash
- **src/generate_images.py** -> script para geração de imagens ilustrativas de proposições dos deputados utilizando o modelo stable-diffusion-v1-4
- **src/vectors.py** -> script para geração dos vetores com base nos dados dos deputados e função para chat com assistente com o modelo gemini-1.5-flash

### diretório data
Gerado no exercício 2, de criação de Textos com LLMs:
- **data/config.yaml** -> Resultado do modelo contendo explicação da Câmara dos Deputados em formato YAML gerado pelo modelo GPT-4o-Mini

Gerado no exercício 3, de processamento dos dados de deputados
- **data/deputados.parquet** -> Base em formato parquet dos deputados
- **data/insights_distribuicao_deputados.json** -> Insights sobre distribuição dos deputados por partido gerado pelo gemini-1.5-flash. Consta no dashboard e alimenta o contexto do assistente

Gerado no exercício 4, de processamento dos dados de despesas 
- **data/despesas_deputados.parquet** -> Base em formato parquet das despesas dos deputados
- **data/insights_despesas_deputados.json** -> Insights sobre as despesas dos deputados das proposições gerado pelo gemini-1.5-flash. Consta no dashboard e alimenta o contexto do assistente

Gerado no exercício 5, de processamento dos dados de proposições
- **data/proposicoes_deputados.parquet** -> Base em formato parquet das proposições dos deputados
- **data/sumarizacao_proposicoes.json** -> Sumarização das proposições gerado pelo gemini-1.5-flash. Consta no dashboard e alimenta o contexto do assistente

Gerado no exercício 8, de assistente online com base vetorial:
- **data/textos_faiss.json** -> Índexes do Facebook AI Similarity Search (FAISS) da base de contexto do assistente
- **data/faiss_index.bin** -> Gerado no exercicio 8, de assistente online com base vetorial, são os textos associados ao FAISS da base de contexto do assistente.

Gerado no exercicio 9, de geração de Imagens com Prompts, são as imagens que representam duas proposições, em estilos e composições diferentes: Gerados pelo stable-diffusion-v1-4
- **data/proposicao_1_versao_1_estilo_ilustração_de_jornal_composicao_imagem_única_centralizada.png**
- **data/proposicao_1_versao_2_estilo_pintura_a_óleo_composicao_imagens_justapostas_no_estilo_colagem.png**
- **data/proposicao_1_versao_3_estilo_desenho_a_lápis_composicao_uma_sequência_de_imagens_minimalistas.png**
- **data/proposicao_2_versao_1_estilo_ilustração_de_jornal_composicao_imagem_única_centralizada.png**
- **data/proposicao_2_versao_2_estilo_pintura_a_óleo_composicao_imagens_justapostas_no_estilo_colagem.png**
- **data/proposicao_2_versao_3_estilo_desenho_a_lápis_composicao_uma_sequência_de_imagens_minimalistas.png**

### diretório docs
Gerada no exercício 1, de arquitetura da Solução
- **docs/diagrama_aplicacao.jpg** -> Desenho da arquitetura da solução
Gerada no exercício 3, de processamento dos dados de deputados
- **docs/distribuição_deputados.png** -> Gráfico de pizza com o total e o percentual de deputados de cada partido. utilizado em dashboard.py

### diretório poe
Geradas no exercício 2, de criação de Textos com LLMs.
prompts pedindo explicação da Câmara dos Deputados no Poe.com:
- **prompt_claude.png** -> modelo Claude-3-Haiku
- **prompt_gemini.png** -> modelo Gemini-1.5-Flash
- **prompt_gpt.png** -> modelo GPT-4o-Mini
- **prompt_gpt_yaml.png** -> modelo GPT-4o-Mini, gerado em formato YAML, salvo em data/config.
