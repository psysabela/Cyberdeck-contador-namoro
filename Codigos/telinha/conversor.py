import os
import re
from PIL import Image

PASTA_IMAGENS = "frames"

frames_bytes = []
largura_final = None
altura_final = None

# Função para ordenar numericamente (ex: frame_2 antes de frame_10)
def chave_ordenacao(nome):
    numeros = re.findall(r"\d+", nome)
    return int(numeros[-1]) if numeros else nome

arquivos = [f for f in os.listdir(PASTA_IMAGENS) if f.lower().endswith(".png")]
if not arquivos:
    print(f"Nenhum arquivo .png encontrado na pasta '{PASTA_IMAGENS}'.")
    exit()

arquivos.sort(key=chave_ordenacao)

for nome_arquivo in arquivos:
    caminho = os.path.join(PASTA_IMAGENS, nome_arquivo)
    img = Image.open(caminho).convert("1")
    w, h = img.size

    # Define a resolução base pelo primeiro frame e valida os seguintes
    if largura_final is None:
        largura_final, altura_final = w, h
    elif (w, h) != (largura_final, altura_final):
        print(f"Aviso: {nome_arquivo} tem tamanho {w}x{h}, esperado {largura_final}x{altura_final}. Redimensionando...")
        img = img.resize((largura_final, altura_final))

    # img.tobytes() gera os bytes no padrão exato do MONO_HLSB
    frames_bytes.append(img.tobytes())

# Grava o arquivo para ser transferido à Pico
with open("animacao.py", "w") as f:
    f.write(f"LARGURA = {largura_final}\n")
    f.write(f"ALTURA = {altura_final}\n")
    f.write(f"FRAMES = {repr(frames_bytes)}\n")

bytes_por_frame = len(frames_bytes[0])
total_kb = (bytes_por_frame * len(frames_bytes)) / 1024

print(f"Sucesso! {len(frames_bytes)} frames convertidos em 'animacao.py'.")
print(f"Resolução: {largura_final}x{altura_final} | Tamanho total dos frames: {total_kb:.2f} KB")