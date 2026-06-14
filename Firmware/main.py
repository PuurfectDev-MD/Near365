import lvgl as lv
import time
import random
from setup_test import System_Init, Controls
from pages.router import UIRouter
from machine import Pin
import uasyncio
import context
from actions.play_tone import play_tone
from actions.helper import list_all_songs, connect_to_wifi, get_time, get_today_present


last_states = [False, False, False, False]

hardware_controls = Controls()
print("Initiated inputs")
time.sleep_ms(300)
if not hardware_controls.is_btn1_pressed: #override the wifi connnection logic- for testing
    context.wifi_connected = connect_to_wifi()
    get_time()
    get_today_present()
else:
    print("Did not try to connect to the internet. No time loaded. No present loaded")
    context.wifi_connected = False

system = System_Init()
system.run_all()
time.sleep_ms(100)
print("System init done")

current_states=[context.wifi_connected,system.sd_mounted,bool(context.today_present),bool(context.current_date)]
                    #wifi connected?          sdcard all good?      present loaded?           date loaded?


context.i2s_bus = system.i2s

router = UIRouter()
router.navigate_to("home")

list_all_songs()
print("System successfully initialized")


async def ui_states_refresher(router):
    import context
    current_angle = 0
    while True:
        # Check if a progress bar exists and is active on the current screen
        if hasattr(router, 'active_progress_bar') and router.active_progress_bar:
            try:
                current_val = getattr(context, 'current_progress', 0)
                router.active_progress_bar.set_value(current_val,0)
            except Exception:
                pass
        
        if hasattr(router, "active_spinning_cd") and router.active_spinning_cd:  #rotates the cd if the obj exits
            if context.play.is_set(): #only if the music is playing
                try:
                    current_angle = (current_angle + 120) % 3600
                    router.active_spinning_cd.set_style_transform_rotation(current_angle, 0)
                except Exception:
                    pass
        if hasattr(router, "active_anim_bars") and router.active_anim_bars:
            try:
                for bar in router.active_anim_bars:
                    new_height = random.randint(30, 80)
                    bar.set_height(new_height)
            except Exception:
                pass
            
        if last_states != current_states:  #checks wether states changed for features and updates the UI.
            try:
                old_wifi, old_sd, old_gift, old_clock = last_states
                new_wifi, new_sd, new_gift, new_clock = current_states
                
                if old_wifi != new_wifi:
                    context.home_logo_objs[0].set_style_text_color(lv.color_hex(0x228B22), 0)
                if old_sd != new_sd:
                    context.home_logo_objs[1].set_style_text_color(lv.color_hex(0x228B22),0)
                if old_gift != new_gift:
                    context.home_logo_objs[2].set_style_line_color(lv.color_hex(0x228B22),0)
                if old_clock != new_clock:
                    context.home_logo_objs[3].set_style_line_color(lv.color_hex(0x228B22),0)
            except:
                pass
                
                
        await uasyncio.sleep_ms(800)
        


async def monitor_buttons():
    print("Monitoring buttons states")
    
    debounce_delay = 250
    last_action_time = 0
    
    last_btn1_state = False
    last_btn1_state= False
    last_en_sw_state = False
    
    last_encoder_val = hardware_controls.encoder_value
    
    while True:
        btn1_pressed = hardware_controls.is_btn1_pressed()
        btn2_pressed = hardware_controls.is_btn2_pressed()
        sw_pressed = hardware_controls.is_en_sw_pressed()
        
        encoder_changed = hardware_controls.read_encoder()
        current_time = time.ticks_ms()
        
        if encoder_changed:
            current_val = hardware_controls.encoder_value
            direction = current_val - last_encoder_val
            
            if direction != 0:
                print(f"direction = {current_val} - {last_encoder_val} = {direction}")
                
                if direction > 0:
                    router.process_input(cw=True)
                else:
                    router.process_input(acw=True)
                    
                last_encoder_val = current_val
                

        if time.ticks_diff(current_time, last_action_time) > debounce_delay:
            if btn1_pressed:
                print("Button 1 pressed")
                last_action_time = current_time
                await play_tone()
                router.process_input(btn1=True)
                
            if btn2_pressed:
                print("Button 2 pressed")
                last_action_time = current_time
                await play_tone()
                router.process_input(btn2= True)
            
            if sw_pressed:
                print("En SW pressed")
                last_action_time = current_time
                router.process_input(sw=True)
                
        await uasyncio.sleep_ms(5)
     
     
async def refresh_lvgl():
    while True:
        lv.timer_handler()
        await uasyncio.sleep_ms(10)
        
async def main():
    uasyncio.create_task(monitor_buttons())
    uasyncio.create_task(refresh_lvgl())
    uasyncio.create_task(ui_states_refresher(router))
    
    while True:
        await uasyncio.sleep_ms(1000)
        
    
uasyncio.run(main())
    
            
        
        
        
        