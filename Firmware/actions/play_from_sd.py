import os
from machine import SPI, Pin, I2S
import uasyncio

async def play_music_from_file(filepath):
    import context
    from context import i2s_bus as audio_out
  
    try:
        path = f"/sd/{filepath}"
        context.current_progress = 0
        swriter = uasyncio.StreamWriter(audio_out)
        
        total_bytes = os.stat(path)[6]
        bytes_played= 44
        
        print("Playing the file at: " , path)
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
                    print("Finished playing the file. Replaying the song")
                    _ = wav_file.seek(44)
                    bytes_played = 44
                    context.current_progress = (bytes_played *100) // total_bytes
                else:
                    swriter.out_buf = wav_samples_mv[:num_read]
                    bytes_played +=num_read             
                    context.current_progress = (bytes_played * 100) // total_bytes
                    
                    await swriter.drain()
                    await uasyncio.sleep_ms(0)
                    
            
    except Exception as e:
        print("Erorr:", e)
        
















