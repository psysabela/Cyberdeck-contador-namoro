import os
from PIL import Image

# Nome da pasta onde estão os arquivos .png extraídos
PASTA_IMAGENS = "frames" 

frames_bytes = []
largura_final = None
altura_final = None

# Lista e ordena os arquivos (ex: frame_01.png, frame_02.png...)
arquivos = sorted([f for f in os.listdir(PASTA_IMAGENS) if f.lower().endswith(".png")])

for nome_arquivo in arquivos:
    caminho = os.path.join(PASTA_IMAGENS, nome_arquivo) 
    
    # Abre a imagem e converte para 1-bit P&B puro
    img = Image.open(caminho).convert("1")
    largura_final, altura_final = img.size

    # Monta o array de bytes no formato MONO_HLSB
    buffer = bytearray()
    for y in range(altura_final):
        byte = 0
        bit_idx = 7
        for x in range(largura_final):
            pixel = img.getpixel((x, y))
            if pixel > 0:  # Pixel aceso (branco)
                byte |= (1 << bit_idx)
            bit_idx -= 1
            if bit_idx < 0:
                buffer.append(byte)
                byte = 0
                bit_idx = 7
        if bit_idx != 7:
            buffer.append(byte)

    frames_bytes.append(bytes(buffer))

# Salva tudo direto em um arquivo pronto para ir para a Pico
with open("animacao.py", "w") as f:
    f.write(f"LARGURA = {largura_final}\n")
    f.write(f"ALTURA = {altura_final}\n")
    f.write(f"FRAMES = {repr(frames_bytes)}\n")

print(f"Sucesso! {len(frames_bytes)} frames convertidos em 'animacao.py'.")