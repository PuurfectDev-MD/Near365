import uasyncio 
i2s_bus = None
sdcard = None


play = uasyncio.Event()

songs_list= []

volume =100
