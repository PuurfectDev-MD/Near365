
import time
from machine import Pin


sw = Pin(18, Pin.IN, Pin.PULL_UP)

while True:
    swVal = sw.value()
    
    print(swVal)
    
    time.sleep(0.2)
