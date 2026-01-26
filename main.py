import uasyncio as asyncio
import time
from machine import Pin
from setup import System_Init, Controls
from setup import WIFI_SSID, WIFI_PASS
import network

WHITE = 0xFFFF
BLACK = 0x0000

working = False
main_button = Pin(48, Pin.IN)  # active LOW - the ttp223 module for on/off signal
current_page = "Menu"  # Holds the active page instance

system = System_Init()



from pages.daily import Daily
from pages.music_player import Music_player
from pages.record_audio import Record
from pages.history import History



saved_time = []
ArcadePix = XglcdFont('ArcadePix9x11.c', 9, 11)

daily_page = Daily(system)

async def wait_for_power_button():
    global working
    while not working:
        if main_button.value() == 1:
            working = True
            print("Device activated")
            system.display.draw_text(100, 110, "BOOTING...", WHITE)
            await asyncio.sleep_ms(300) 
            break
        await asyncio.sleep_ms(50)



async def state_monitor():
    """Monitor power button to shut down device."""
    global working
    while True:
        if working and main_button.value() ==1 :
            print("Power OFF triggered.")
            working = False
            system.display.fill_hrect(0, 0, 320, 240, BLACK)
            await asyncio.sleep_ms(300)
            break
        await asyncio.sleep_ms(200)







async def main_loop():
    last_selection = 0
    confirmed_item = None

    print("Menu Active: Select 1-4")

    while True:
        # 1. Handle Navigation (Rotation)
        if system.controls.read_encoder():
            current_selection = system.controls.map_encoder_values(4)
            
            # Only redraw if the selection actually changed
            if current_selection != last_selection:
                print(f"Highlighting Menu Item: {current_selection}")
                #  change text color of the background of this menu element- ---for later
                last_selection = current_selection

        # Handle Confirmation (Button Press)
        if system.controls.is_pressed():
            confirmed_item = system.controls.map_encoder_values(4)
            print(f"USER CONFIRMED: {confirmed_item}")
            
            # Perform action
            if confirmed_item == 1: 
                today = get_time()
                await daily_page.run_page_loop(today)  #runs unitl btn2 is pressed
                draw_menu() #immediately updates to the menu
            elif confirmed_item == 2:
                Music_player.play_music()
            elif confirmed_item ==3:
                Record.record_voice()
            elif confirmed_item ==4:
                History.show_past_msg()
            await asyncio.sleep_ms(500) 

        await asyncio.sleep_ms(20)


async def setup_and_run():
    system.run_all()
    connect_wifi()
    draw_menu() 
    await asyncio.gather(
        wait_for_power_button(),
        state_monitor(),
        main_loop()
    )
    


try:
    asyncio.run(setup_and_run())
except KeyboardInterrupt:  #for testing
    print("Clean shutdown")




def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    print("Connecting to Wi-Fi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\n✅ Connected:", wlan.ifconfig())
    

def get_time():
    global saved_time
    for attemps in range(3):
        try:
            time_tuple = system.rtc.get_time() #this give a tuple
            year, month, day, hour, minute, second = time_tuple[:6]
            saved_time =[year,month,day]
            # Format: 2026-01-26
            timestamp_str = "{:04d}-{:02d}-{:02d}".format(year, month, day)  #saved into a string which I will use in my json file for searching 
            return timestamp_str
        except Exception as e:
            print(f"{e} Coundlt get time")


def draw_menu():
    system.display.draw_text(100,20,"Present",ArcadePix,WHITE)
    system.display.draw_text(100,50,"Music",ArcadePix,WHITE)
    system.display.draw_text(100,100,"Memo",ArcadePix,WHITE)
    system.display.draw_text(100,150,"History",ArcadePix,WHITE)