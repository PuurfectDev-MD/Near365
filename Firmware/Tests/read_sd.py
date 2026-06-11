import os
from machine import Pin, SPI 
import sdcard

CS_PIN   = 10   
SCK_PIN  = 12
MOSI_PIN = 11 
MISO_PIN = 13  

cs = Pin(CS_PIN, Pin.OUT, value=1)

spi = SPI(1, baudrate=10000000, polarity=0, phase=0, 
          sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))

try:
    print("Connecting to SD card")
    sd = sdcard.SDCard(spi, cs)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    print("Success")

    file_path = "/sd/test.txt"
    print(f"Opening and reading {file_path}:\n")
    with open(file_path, "r") as f:
        print(f.read())
    print("Read operation complete!")

except OSError as e:
    print("\n Error encountered:", e)

finally:
    try:
        os.unmount("/sd")
    except:
        pass