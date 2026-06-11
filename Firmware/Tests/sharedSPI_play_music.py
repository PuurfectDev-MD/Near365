import time
import os
import sdcard
from machine import SPI, Pin, I2S
from xglcd_font import XglcdFont
from ili9341 import Display

bits = 16
sample_rate = 22050  # or 44100


I2S_DOUT = 7
I2S_BCLK = 6
I2S_LRC = 5
EN_PIN = Pin(41, Pin.OUT, value=1)

SPI_MOSI = 11
SPI_MISO = 13
SPI_SCK = 12

TFT_CS = 1
TFT_DC = 2
TFT_RST = 42
TFT_BL = 4
SD_CS = 10


WHITE = 0xFFFF
BLACK = 0x0000


tft_cs_pin = Pin(TFT_CS, Pin.OUT, value=1)
sd_cs_pin = Pin(SD_CS, Pin.OUT, value=1)

shared_spi = SPI(2, baudrate=10000000, polarity=0, phase=0, 
                 sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))

Pin(TFT_BL, Pin.OUT).value(1)


ArcadePix = XglcdFont('ArcadePix9x11.c', 9, 11)

display = Display(shared_spi,
                  cs=tft_cs_pin,
                  dc=Pin(TFT_DC),
                  rst=Pin(TFT_RST),
                  width=320,
                  height=240,
                  rotation=270)

time.sleep_ms(100)
 
print("The TFT screen was initialized")
display.fill_rectangle(0, 0, 320, 240, WHITE)
display.fill_circle(100, 120, 25, BLACK)
display.draw_text(110, 110, "BOOTING DONE!", ArcadePix, BLACK)

time.sleep(2)
print("The display is over... now over to audio from sd card")

audio_out = I2S(1, 
                sck=I2S_BCLK,
                ws=I2S_LRC,
                sd=I2S_DOUT,
                bits=bits,
                mode=I2S.TX,
                format=I2S.MONO,
                rate=sample_rate,
                ibuf=2048)

print("SPI AND I2S init done!")


try:
    sd = sdcard.SDCard(shared_spi, sd_cs_pin)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    print("SD card mounted successfully")
    
    wav_path = "/sd/01.wav"
    
    with open(wav_path, "rb") as wav_file:
        # Skip the 44-byte WAV header
        wav_file.seek(44)
        print("Playing audio chunks...")
        
        chunk_size = 1024
        while True:
            audio_chunk = wav_file.read(chunk_size)
            
            if not audio_chunk:
                break  
                
            audio_out.write(audio_chunk)
            
        
        display.draw_text(110, 110, "Finished playing the wav file :)", ArcadePix, BLACK)
        print("Playback finished cleanly.")
        
except Exception as e:
    print("Error encountered:", e)
    
finally:
    print("Cleaning up resources...")
    EN_PIN.value(0) 
    
    if 'audio_out' in locals():
        audio_out.deinit()
        
    try:
        os.unmount("/sd")
        print("SD card unmounted.")
    except Exception:
        pass