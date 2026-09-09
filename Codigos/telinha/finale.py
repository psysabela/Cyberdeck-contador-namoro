from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import animacao

# Inicializa o barramento I2C e botão
botao = Pin(16, Pin.IN, Pin.PULL_UP)
i2c = I2C(1, scl=Pin(27), sda=Pin(26), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Data atual que será usada para calcular a diferença em dias desde a data inicial
# Formato: (ano, mes, dia, dia_da_semana, hora, min, seg, subseg)
rtc = RTC()
rtc.datetime((2026, 9, 9, 2, 10, 25, 0, 0)) # Exemplo: 09/09/2026

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
total_frames = len(frames)

def exibir_contador():
    t_atual = rtc.datetime()
    seg_inicio = utime.mktime((2025, 6, 4, 17, 0, 0, 0, 0))
    seg_atual = utime.mktime((t_atual[0], t_atual[1], t_atual[2], t_atual[4], t_atual[5], t_atual[6], 0, 0))
    
    diferenca = seg_atual - seg_inicio
    
    dias = diferenca // 86400
    horas = (diferenca % 86400) // 3600
    minutos = (diferenca % 3600) // 60
    segundos = diferenca % 60
    
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)  # Borda
    
    oled.text("Juntos ha:", 28, 10)
    
    # Linha 1: Dias em destaque
    txt_dias = f"{dias} DIAS"
    x_dias = (128 - (len(txt_dias) * 8)) // 2
    oled.text(txt_dias, x_dias, 24)
    
    # Linha 2: Horas, minutos e segundos correndo
    txt_relogio = f"{horas:02d}h {minutos:02d}m {segundos:02d}s"
    x_rel = (128 - (len(txt_relogio) * 8)) // 2
    oled.text(txt_relogio, x_rel, 38)
    
    oled.text("<3", 56, 51)
    oled.show()

# Variáveis de controle do estado da tela
estado = "DESLIGADO"
ultimo_estado_botao = 1
idx_frame = 0

while True:
    leitura_botao = botao.value()
    # Detecta o clique quando o botao fecha contato com o terra (1 -> 0)
    clicou = (ultimo_estado_botao == 1 and leitura_botao == 0)
    ultimo_estado_botao = leitura_botao

    # ESTADO A: DISPLAY APAGADO
    if estado == "DESLIGADO":
        if clicou:
            oled.poweron()
            idx_frame = 0
            estado = "ANIMANDO"
            utime.sleep_ms(200)  # Debounce

    # ESTADO B: REPRODUZINDO FRAMES
    elif estado == "ANIMANDO":
        oled.fill(0)
        oled.blit(frames[idx_frame], pos_x, pos_y)
        oled.show()
        
        idx_frame += 1

        # Ao chegar no final, troca para a tela do contador
        if idx_frame >= total_frames:
            exibir_contador()
            estado = "CONTADOR"
            utime.sleep_ms(200)
        else:
            utime.sleep_ms(frame_delay_ms)

    # ESTADO C: TELA FIXA DO CONTADOR
    elif estado == "CONTADOR":
        if clicou:
            oled.fill(0)
            oled.show()
            oled.poweroff()
            estado = "DESLIGADO"
            utime.sleep_ms(250)  # Debounce
        else:
            # Redesenha a tela para atualizar o relógio continuamente
            exibir_contador()
            utime.sleep_ms(100)