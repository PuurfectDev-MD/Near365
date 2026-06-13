import uasyncio 
i2s_bus = None
sdcard = None


play = uasyncio.Event()


songs_list= [] #from sd card

volume =100

song_focused_index = 0 #current focused item
music_list_objs = [] #from lv's buttons objs for focus switch
now_playing_index= 0 # currenly playing song
current_progress =0  #for the music progress bar


audio_task = None #to store the current playing event


playing_title_obj = None
playing_time_obj = None

today_present = {}
SSID = "mylaptop"
PASS= "connecttest"
API_URL = "https://timeapi.io/api/v1/time/current/utc"
current_date = ""


