import math
import array
import time
from machine import I2S, Pin

print("Start")

MAX98357_LRC = 5
MAX98357_BCLK = 6
MAX98357_DIN =7

i2s = I2S(0,
          sck=Pin(MAX98357_BCLK),
          ws=Pin(MAX98357_LRC),
          sd=Pin(MAX98357_DIN),
          mode=I2S.TX,
          bits=16,
          format=I2S.MONO,
          rate=44100,
          ibuf=44100,
          )
print("i2s:", i2s)

def generate_tone(sample_rate, frequency, duration):
    tick_ms_generate_tone_start = time.ticks_ms()
    sample_count = int(sample_rate * duration)
    amplitude = 14000 #32767
    wave = array.array("h", (0 for _ in range(sample_count)))
    for i in range(sample_count):
        wave[i] = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
    tick_ms_generate_tone_end = time.ticks_ms()
    print("Time to generate Tone", frequency, "Hz for", duration,
          "s with sample_rate", sample_rate, "=", "ms",
          time.ticks_diff(tick_ms_generate_tone_end, tick_ms_generate_tone_start))
    return wave


duration = 1
tone_1k5 = generate_tone(44100, 1500, duration)

def play_tone():
    print("Play single tone")
    tick_ms_i2s_write_start = time.ticks_ms()
    i2s.write(tone_1k5)
    tick_ms_i2s_write_end = time.ticks_ms()
    print("Time for i2s.write()", ":",
          time.ticks_diff(tick_ms_i2s_write_end, tick_ms_i2s_write_start), "ms")
    time.sleep(duration)
    print("Playing stop")

play_tone()

while True:
    k = input("'q' to quit, others re-play tone.")
    if k == 'q':
        break
    play_tone()

print("~ bye ~")
i2s.deinit()