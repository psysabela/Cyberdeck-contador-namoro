from machine import Pin
import utime

# Configura o botão com pull-up no GPIO 16
botao = Pin(16, Pin.IN, Pin.PULL_UP)

# Configura o LED embutido da Pico
try:
    led = Pin("LED", Pin.OUT)  # Pico W / firmware recente
except TypeError:
    led = Pin(25, Pin.OUT)     # Pico clássica (GPIO 25)

print("Monitorando o botao... Pressione para testar (Ctrl+C para sair)")

while True:
    val = botao.value()
    # Quando pressionado, o valor cai para 0
    if val == 0:
        led.value(1)
        print("BOTAO PRESSIONADO! (Valor: 0)")
    else:
        led.value(0)
    utime.sleep_ms(100)