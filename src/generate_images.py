import torch
from diffusers import DiffusionPipeline
import json
from IPython.display import Image

# Set device
device = (
    "mps"
    if torch.backends.mps.is_available()
    else "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

# Load the pipeline
pipe = DiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", token="").to(device)

# Load summarized propositions
with open("data/sumarizacao_proposicoes.json", "r", encoding="utf-8") as f:
    proposicoes_resumo = json.load(f)

projeto_1 = proposicoes_resumo[19]['sumarizacao']
projeto_2 = proposicoes_resumo[25]['sumarizacao']

# Predefined styles and compositions
styles_and_compositions = [
    {"estilo": "ilustração de jornal", "composicao": "imagem única centralizada"},
    {"estilo": "pintura a óleo", "composicao": "imagens justapostas no estilo colagem"},
    {"estilo": "desenho a lápis", "composicao": "uma sequência de imagens minimalistas"}
]

def gerar_imagens_proposicoes(seed=None):
    for idx, projeto in enumerate((projeto_1, projeto_2), 1):
        for version, config in enumerate(styles_and_compositions, 1):
            estilo = config["estilo"]
            composicao = config["composicao"]

            print(f"Projeto {idx} - Versão {version}: {projeto}")
            print(f"Estilo: {estilo}")
            print(f"Composição: {composicao}")

            pipe_args = {
                "prompt":f"{estilo} com {composicao} que ilustre: {projeto}",
                "negative_prompt":"baixa resolução, incompreensível, abstrato",
                "guidance_scale":15,
                "height":480,
                "width":640,
            }

            if seed is not None:
                pipe_args["generator"] = torch.Generator("cuda").manual_seed(seed)

            image = pipe(**pipe_args).images[0]

            file_name = f"data/proposicao_{idx}_versao_{version}_estilo_{estilo.replace(' ', '_')}_composicao_{composicao.replace(' ', '_')}.png"
            image.save(file_name)

            # Display the image
            display(Image(file_name))
