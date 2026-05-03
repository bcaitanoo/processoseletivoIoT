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

# CONFIGURAÇÃO DO LED RBG
led_azul = Pin(25, Pin.OUT)
led_verde = Pin(26, Pin.OUT)
led_vermelho = Pin(27, Pin.OUT)

# Função responsável por indicar o estado da temperatura via LED
def definir_leds(temp):
    if temp <= 10: # Temperatura menor ou igual a 10ºC o led fica azul
        led_azul.value(1)
        led_verde.value(0)
        led_vermelho.value(0)
    elif temp < 30: # Temperatura menor que 30ºC e maior que 10ºC o led fica verde
        led_azul.value(0)
        led_verde.value(1)
        led_vermelho.value(0)
    else: # Temperatura maior ou igual a 30ºC o led fica vermelho
        led_azul.value(0)
        led_verde.value(0)
        led_vermelho.value(1)

# LOOP PRINCIPAL
while True :
  ds_sensor.convert_temp() # Conversão da temperatura do sensor 
  time.sleep_ms(750) # Tempo de leitura do sensor

  temperatura = ds_sensor.read_temp(sensor_analisado) # Lê temperatura convertida
  print("Temperatura:", temperatura, "°C")
  definir_leds(temperatura)  # Atualiza LED conforme a temperatura

  # Atualiza apenas a segunda linha do display (valor da temperatura) com formatação para evitar residuos
  lcd.move_to(0, 1)
  lcd.putstr("{:<16}".format("{:>5.1f} C".format(temperatura)))