import os
from machine import Pin, I2S, SPI
import time
from sdcard import SDCard

# ======= SD CARD HARDWARE CONFIGURATION =======
SD_MOSI = 9
SD_MISO = 8
SD_SCK = 3
SD_CS_PIN = 10

AMP_SD = Pin(41, Pin.OUT)

# ======= I2S MICROPHONE & SPEAKER HARDWARE =======
SCK_PIN = 6
WS_PIN = 5
SD_PIN = 15

record_pin = Pin(39, Pin.IN, Pin.PULL_UP)
samples = bytearray(512)

def wait_for_button():
    while record_pin.value() == 1:
        time.sleep_ms(100)
    time.sleep_ms(100)


sd_cs = Pin(SD_CS_PIN, Pin.OUT)
spi = SPI(1, baudrate=1320000, sck=Pin(SD_SCK), mosi=Pin(SD_MOSI), miso=Pin(SD_MISO))
sd = SDCard(spi, sd_cs)
vfs = os.VfsFat(sd)
os.mount(vfs, "/sd")

print("Press the button to record")
wait_for_button()

AMP_SD.value(0) 
print("Recording now")

audio_in = I2S(0, sck=Pin(SCK_PIN), ws=Pin(WS_PIN), sd=Pin(SD_PIN), mode=I2S.RX, bits=16, format=I2S.MONO, rate=16000, ibuf=4096)

with open("/sd/test.raw", "wb") as file:
    while record_pin.value() == 0:
        read_bytes = audio_in.readinto(samples)
        if read_bytes > 0:
            I2S.shift(buf=samples, bits=16, shift=4)
            file.write(samples[:read_bytes])

audio_in.deinit()
print("Recording is done. press to play.")

wait_for_button()

AMP_SD.value(1) 
time.sleep(0.5)
print("Playing back")
audio_out = I2S(0, sck=Pin(SCK_PIN), ws=Pin(WS_PIN), sd=Pin(SD_PIN), mode=I2S.TX, bits=16, format=I2S.STEREO, rate=16000, ibuf=4096)

with open("/sd/test.raw", "rb") as file:
    samples_read = file.readinto(samples)
    while samples_read > 0:
        audio_out.write(samples[:samples_read])
        samples_read = file.readinto(samples)

audio_out.deinit()
AMP_SD.value(0)

print("The playback finished")