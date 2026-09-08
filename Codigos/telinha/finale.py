from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import animacao

# Inicializa o barramento I2C 
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

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

# Loop contínuo da animação
while True:
    for fb in frames:
        oled.fill(0)                  # Limpa o frame anterior
        oled.blit(fb, pos_x, pos_y)   # Desenha o frame atual centralizado
        oled.show()                   # Atualiza o display OLED
        utime.sleep_ms(frame_delay_ms)