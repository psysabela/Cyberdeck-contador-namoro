from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import animacao

# Inicializa o barramento I2C e botão
botao = Pin(16, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Força a tela a iniciar apagada imediatamente
oled.fill(0)
oled.show()
oled.poweroff()

# Monta a lista de frames na memória
frames = [
    framebuf.FrameBuffer(bytearray(f), animacao.LARGURA, animacao.ALTURA, framebuf.MONO_HLSB)
    for f in animacao.FRAMES
]

# Centraliza a animação no display de 128x64
pos_x = (128 - animacao.LARGURA) // 2
pos_y = (64 - animacao.ALTURA) // 2

# Delay entre frames em milissegundos (170ms = ~5.9 FPS)
frame_delay_ms = 170

# Variáveis de controle
tela_ligada = False       # Inicia em estado desligado
ultimo_estado_botao = 1
idx_frame = 0
total_frames = len(frames)

while True:
    # Verifica o estado do botão
    if botao.value() == 0:  # Botão pressionado
        oled.poweron()  # Liga a tela
        for frame in frames:
            oled.fill(0)  # Limpa a tela
            oled.blit(frame, pos_x, pos_y)  # Desenha o frame atual
            oled.show()  # Atualiza a tela
            utime.sleep_ms(frame_delay_ms)  # Aguarda o tempo do frame
    else:
        oled.fill(0)
        oled.show()
        oled.poweroff() 
        utime.sleep_ms(250) # Debounce mecânico contra ruídos do botão

# Se ligada, anima os frames
    if tela_ligada:
        oled.fill(0)
        oled.blit(frames[idx_frame], pos_x, pos_y)
        oled.show()

        idx_frame = (idx_frame + 1) % total_frames
        utime.sleep_ms(frame_delay_ms)
    else:
        # Quando desligada, dorme um tempo curto para economizar processamento
        utime.sleep_ms(40)