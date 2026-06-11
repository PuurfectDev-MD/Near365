import os
from machine import I2S
from machine import Pin



WAV_FILE = "wav_file.wav"
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.STEREO
SAMPLE_RATE_IN_HZ = 8000

wav = open(WAV_FILE, "rb")
pos = wav.seek(44)  


wav_samples = bytearray(1000)
wav_samples_mv = memoryview(wav_samples)

def playWavFromFlash():
    try:
        from context import i2s_bus as audio_out
        while True:
            num_read = wav.readinto(wav_samples_mv)
            # end of WAV file?
            if num_read == 0:
                wav.close()
                break
            else:
                _ = audio_out.write(wav_samples_mv[:num_read])

    except (Exception) as e:
        print("caught exception {} {}".format(type(e).__name__, e))



