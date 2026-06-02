
import time
from machine import Pin

# Configure GPIO 38 and 39 as inputs with internal pull-up resistors
switch_38 = Pin(38, Pin.IN, Pin.PULL_UP)
switch_39 = Pin(39, Pin.IN, Pin.PULL_UP)

print("Reading switches... Press Ctrl+C in Thonny to stop.")
print("--------------------------------------------------")

while True:
    # Read the current digital value (0 or 1) of each pin
    val_38 = switch_38.value()
    val_39 = switch_39.value()
    
    # Print the values clearly on the same line
    print(f"Switch 38: {val_38} | Switch 39: {val_39}")
    
    # Delay slightly so the Thonny terminal doesn't scroll too fast
    time.sleep(0.2)
