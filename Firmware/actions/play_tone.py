import math
import array
import time
import uasyncio
import context

tone_buffer = None

def pre_generate_tone(sample_rate=22050, frequency=1500, duration=0.1):
    global tone_buffer
    sample_count = int(sample_rate * duration)
    amplitude = 14000 
    tone_buffer = array.array("h", (0 for _ in range(sample_count)))
    
    for i in range(sample_count):
        tone_buffer[i] = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
    print(f"Audio buffer initialized: {frequency}Hz tone ready in RAM.")

pre_generate_tone()

async def play_tone():
    if not context.play.is_set():
        global tone_buffer
        if tone_buffer is None:
            return

        i2s = context.i2s_bus 
        if i2s is None:
            return
        
        try:
            swriter = uasyncio.StreamWriter(i2s)
            swriter.out_buf = memoryview(tone_buffer)
            await swriter.drain()
        except Exception as e:
            print("I2S Feedback Error:", e)
        finally:
                
            await uasyncio.sleep_ms(0)
    

