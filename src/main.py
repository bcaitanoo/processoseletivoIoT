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

# DETECÇÃO DO SENSORES CONECTADOS E SELEÇÃO DO PRIMEIRO DA LISTA
sensores_conectados = ds_sensor.scan() 
sensor_analisado = sensores_conectados[0]

# FORMATAÇÃO DO DISPLAY APOS CONEXAO COM SENSOR CONCLUIDA
lcd.clear()
lcd.putstr("Temperatura:")
lcd.move_to(0, 1)
lcd.putstr("00.0 C") 

# LOOP PRINCIPAL
while True :
  ds_sensor.convert_temp() # Conversão da temperatura do sensor 
  time.sleep_ms(750) # Tempo de leitura do sensor

  temperatura = ds_sensor.read_temp(sensor_analisado) # Lê temperatura convertida
  
  # Atualiza apenas a segunda linha do display (valor da temperatura) com formatação para evitar residuos
  lcd.move_to(0, 1)
  lcd.putstr("{:<16}".format("{:>5.1f} C".format(temperatura)))