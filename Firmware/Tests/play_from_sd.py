import os
from machine import SPI, Pin, I2S
import sdcard

mosi_pin = Pin(11)
miso_pin = Pin(13)
sck_pin = Pin(12)


bits= 16
sample_rate = 22050 # or try 44100


I2S_DOUT = 7
I2S_BCLK =6
I2S_LRC =5
EN_PIN= Pin(41,Pin.OUT, value=1)

cs_pin= Pin(10, Pin.OUT, value=1)

            
spi = SPI(1, baudrate=100000, polarity=0, phase=0, sck=sck_pin, mosi=mosi_pin, miso=miso_pin)
audio_out = I2S(1, sck=I2S_BCLK,
                ws=I2S_LRC,
                sd=I2S_DOUT,
                bits=bits,
                mode=I2S.TX,
                format=I2S.MONO,
                rate=sample_rate,
                ibuf=2048)


print("SPI AND I2S init done!")
try:
    sd = sdcard.SDCard(spi, cs_pin)
    vfs = os.VfsFat(sd)
    os.mount(vfs, "/sd")
    
    print("Sd card mounted")
    
    wav_path = "/sd/01.wav"
    
    with open(wav_path, "rb") as wav_file:
        wav_file.seek(44)

        print("Reading audio chunks")
        chunk_size = 1024
        while True:
            audio_chunk= wav_file.read(chunk_size)
            
            if not audio_chunk:
                break
            audio_out.write(audio_chunk)
        print("Finished playing the wav file :)")
        
except Exception as e:
    print("Erorr:", e)
    
finally:
    EN_PIN.value(0) 
    
    if 'audio_out' in locals():
        audio_out.deinit()
    try:
        os.unmount("/sd")
        print("SD card unmounted.")
    except:
        pass
