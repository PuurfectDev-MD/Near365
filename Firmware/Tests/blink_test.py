from machine import Pin
import time

LED1 = Pin(40, Pin.OUT)
LED2 = Pin(16, Pin.OUT)
while True:
    LED1.value(1)
    LED2.value(2) 
    time.sleep(0.5)
    LED1.value(0)
    LED2.value(0)
    time.sleep(0.5)