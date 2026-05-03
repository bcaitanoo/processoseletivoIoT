from machine import Pin, SoftI2C
from i2c_lcd import I2cLcd
import onewire
import ds18x20
import time

# CONFIGURAÇÃO DO SENSOR (DS18B20)
ds_pin = Pin(4) # Define o pino de dados do sensor (barramento OneWire)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin)) # Inicializa o sensor de temperatura

# CONFIGURAÇÃO DO DISPLAY LCD (I2C)
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
lcd = I2cLcd(i2c, 0x27, 2, 16)

# CONFIGURAÇÃO DO LED RBG
led_azul = Pin(25, Pin.OUT)
led_verde = Pin(26, Pin.OUT)
led_vermelho = Pin(27, Pin.OUT)

# FUNÇÃO RESPONSÁVEL POR INDICAR O ESTADO DA TEMPERATURA VIA LED RGB
def definir_leds(temp):
    if temp <= 10: # Temperatura menor ou igual a 10ºC o led fica azul
        led_azul.value(1)
        led_verde.value(0)
        led_vermelho.value(0)
    elif 10 < temp < 30: # Temperatura menor que 30ºC e maior que 10ºC o led fica verde
        led_azul.value(0)
        led_verde.value(1)
        led_vermelho.value(0)
    else: # Temperatura maior ou igual a 30ºC o led fica vermelho
        led_azul.value(0)
        led_verde.value(0)
        led_vermelho.value(1)

print("Inicio do programa")

# DETECÇÃO DO SENSORES CONECTADOS E SELEÇÃO DO PRIMEIRO DA LISTA
sensores_conectados = ds_sensor.scan() # Procura sensores DS18B20 conectados no barramento
sensor_analisado = sensores_conectados[0] # Seleciona o primeiro sensor encontrado
print("Sensor conectado: ", sensor_analisado) 

# FORMATAÇÃO DO DISPLAY APÓS CONEXãO COM SENSOR CONCLUÍDA
lcd.clear()
lcd.putstr("Temperatura:")
lcd.move_to(0, 1)
lcd.putstr("00.0 C") 

# VALORES INICIAS
ultima_leitura = 0
temperatura = 0
ds_sensor.convert_temp()

# LOOP PRINCIPAL
while True:
    leitura_atual = time.ticks_ms() # Tempo atual em ms

    # LEITURA DO SENSOR (a cada 750ms)
    if time.ticks_diff(leitura_atual, ultima_leitura) >= 750:
        temperatura = ds_sensor.read_temp(sensor_analisado) # Lê temperatura após tempo de conversão
        print("Temperatura:", temperatura, "°C") # Mostra temperatura no serial

        # Atualiza apenas a linha do valor no display
        lcd.move_to(0, 1)
        lcd.putstr("{:<16}".format("{:>5.1f} C".format(temperatura)))

        ds_sensor.convert_temp()  # Inicia nova conversão para próxima leitura
        ultima_leitura = leitura_atual # Atualiza referência de tempo

    # CONTROLE NÃO BLOQUEANTE DO LED (pisca em temperaturas extremas)
    if temperatura >= 40: # Pisca vermelho usando controle por tempo se a temperatura for maior que 40ºC
        if (leitura_atual // 125) % 2 == 0:
            led_vermelho.value(1)
        else:
            led_vermelho.value(0)
        led_verde.value(0)
        led_azul.value(0)

    elif temperatura <= -10: # Pisca azul se a temperatura for menor ou igual a -10ºC
        if (leitura_atual // 125) % 2 == 0: 
            led_azul.value(1)
        else:
            led_azul.value(0)
        led_verde.value(0)
        led_vermelho.value(0)

    else: # Se a temperatura não estiver extrema realiza definição normal por função
        definir_leds(temperatura)