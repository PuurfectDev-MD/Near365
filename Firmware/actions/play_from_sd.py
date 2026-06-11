import os
from machine import SPI, Pin, I2S
import uasyncio

async def play_music_first_file():
    import context
    from context import i2s_bus as audio_out
  
    try:
        path = "/sd/01.wav"
        swriter = uasyncio.StreamWriter(audio_out)
        
        with open(path, "rb") as wav_file:
            _ = wav_file.seek(44)
            
            wav_samples = bytearray(10000)
            wav_samples_mv = memoryview(wav_samples)
            
            print("Playing audio file now..>")
            
            while True:
                if not context.play.is_set(): #checks if the play event is false
                    print("Playing is stopped")
                    await context.play.wait() #the loop wont move from here until the event is changed to true
                    
                num_read = wav_file.readinto(wav_samples_mv)
                
                if num_read == 0:
                    print("Finished playing the file")
                    break
                else:
                    swriter.out_buf = wav_samples_mv[:num_read]
                    await swriter.drain()
                    
            
    except Exception as e:
        print("Erorr:", e)
        






