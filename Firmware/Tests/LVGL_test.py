import lvgl as lv
import time
from setup_test import System_Init

# 1. Initialize system and internal drivers
system = System_Init()
system.run_all()
time.sleep_ms(100)

# 2. Get the active display screen that the driver auto-registered
scr = lv.screen_active()

scr.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
scr.set_style_border_width(2, lv.PART.MAIN)
scr.set_style_border_color(lv.palette_main(lv.PALETTE.BLUE), lv.PART.MAIN)

### Style ###################
btnstyle = lv.style_t()
btnstyle.init()
btnstyle.set_radius(5)
btnstyle.set_bg_opa(lv.OPA.COVER)
btnstyle.set_bg_color(lv.palette_main(lv.PALETTE.BLUE))
btnstyle.set_outline_width(2)
btnstyle.set_outline_color(lv.palette_main(lv.PALETTE.BLUE))
btnstyle.set_outline_pad(8)
 
#### Button ##################
btn = lv.button(scr)
btn.set_size(100, 50)
btn.center()
btn.add_style(btnstyle, lv.PART.MAIN)

lbl = lv.label(btn)
lbl.set_text("One")
lbl.center()
lbl.set_style_text_color(lv.color_black(), lv.PART.MAIN)
lbl.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)

cnt = 1

def btn_cb(event):
    global cnt
    print("Clicked button:", cnt)
    cnt = cnt + 1

btn.add_event_cb(btn_cb, lv.EVENT.CLICKED, None)

print("UI configured. Starting background refresh ticker loop...")

# --- THE MANDATORY TICK ENGINE ---
# In LVGL 9, you must continuously call timer_handler to push frame shifts over SPI.
while True:
    lv.timer_handler()
    time.sleep_ms(10)