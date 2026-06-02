from setup_test import System_Init
from machine import Pin
import time
from xglcd_font import XglcdFont


WHITE = 0xFFFF
BLACK = 0x0000

ArcadePix = XglcdFont('ArcadePix9x11.c', 9, 11)
system = System_Init()
system.run_all()
time.sleep_ms(100)
print("The TFT screen was initialized")



system.display.draw_text(110, 220, "BOOTING...", ArcadePix, WHITE)
time.sleep(5)

