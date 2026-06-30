from machine import Pin, SPI
import time
from xglcd_font import XglcdFont
from ili9341 import Display

SPI_MOSI = 11
SPI_MISO = 13
SPI_SCK = 12


TFT_CS = 1
TFT_DC =2
TFT_RST= 42
TFT_BL = 4


WHITE = 0xFFFF
BLACK = 0x0000
Pin(TFT_BL, Pin.OUT).value(1)

ArcadePix = XglcdFont('ArcadePix9x11.c', 9, 11)
spi = SPI(2, baudrate=100000, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))

display = Display(spi,
                  cs=Pin(TFT_CS),
                  dc=Pin(TFT_DC),
                  rst=Pin(TFT_RST),
                  width=320,
                  height=240,
                  rotation=270)

time.sleep_ms(100)
print("The TFT screen was initialized")



display.draw_text(110, 220, "BOOTING...", ArcadePix, BLACK)


display.draw_text(200, 220, "BOOTING...", ArcadePix, WHITE)

print("The display content were drawn")

time.sleep(5)
