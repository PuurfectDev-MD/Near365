import lvgl as lv
import time
from setup_test import System_Init, Controls
from pages.router import UIRouter
from machine import Pin
import uasyncio
import context
from actions.play_tone import play_tone
from actions.helper import list_all_songs

system = System_Init()
system.run_all()
time.sleep_ms(100)
print("System init done")

context.i2s_bus = system.i2s

if context.i2s_bus:
    print("context set")

hardware_controls = Controls()

router = UIRouter()
router.navigate_to("home")

print("System successfully initialized")
list_all_songs()

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
                uasyncio.create_task(play_tone())
                router.process_input(btn1=True)
                
            if btn2_pressed:
                print("Button 2 pressed")
                last_action_time = current_time
                uasyncio.create_task(play_tone())
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
    
    while True:
        await uasyncio.sleep_ms(1000)
        
    
uasyncio.run(main())
    
            
        
        
        
        
