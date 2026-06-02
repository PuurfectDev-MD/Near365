from machine import Pin
import time

LED1 = Pin(40, Pin.OUT)

while True:
    LED1.value(1)
    time.sleep(0.5)
    LED1.value(0)
    time.sleep(0.5)