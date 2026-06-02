import lvgl as lv
import time
from setup_test import System_Init

# 1. Initialize system and internal drivers
system = System_Init()
system.run_all()
time.sleep_ms(100)

# Get the currently active screen object
scr = lv.screen_active()
# Set the screen background color to black
scr.set_style_bg_color(lv.color_hex(0x000000), 0)

# Create a calendar object
calendar = lv.calendar(scr)
# Set size
calendar.set_size(250, 250)
# Center the display
calendar.center()
# Set today's date (October 15, 2023)
calendar.set_today_date(2023, 10, 15)
# Set the currently displayed month
shown_date = lv.calendar_date_t()
shown_date.year = 2023
shown_date.month = 10


# Set year list (2020-2030)
year_list = "\n".join([str(y) for y in range(2020, 2031)])
calendar.header_dropdown_set_year_list(year_list)