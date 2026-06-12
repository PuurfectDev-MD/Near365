import uasyncio 
i2s_bus = None
sdcard = None


play = uasyncio.Event()
play.set()

songs_list= [] #from sd card

volume =100

song_focused_index = 0 #current focused item
music_list_objs = [] #from lv's buttons objs for focus switch

audio_task = None #to store the current playing event

SSID = "mylaptop"
PASS= "connecttest"
API_URL = "https://timeapi.io/api/v1/time/current/utc"

current_date = ""


today_present = []

