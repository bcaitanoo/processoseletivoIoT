from machine import Pin
import onewire
import ds18x20
import time

ds_pin = Pin(21)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

sensores_conectados = ds_sensor.scan()
print("Sensores encontrados: ", sensores_conectados)
while True :
  ds_sensor.convert_temp()
  time.sleep_ms(750)

  for sensor_conectado in sensores_conectados:
    temperatura = ds_sensor.read_temp(sensor_conectado)
    print("Temperatura:", temperatura, "°C")

  time.sleep(1)