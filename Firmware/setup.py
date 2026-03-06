import ili9341
from ili9341 import Display
from ds3231 import DS3231
from machine import I2S
import time
master_file = master.json #file on sd card with all info   - stored on sd card
daily_file = daily.json #file info extracted on this for today (one day) -stored on esp flash



WIFI_SSID = ""
WIFI_PASS = ""


SPI_MOSI = 11
SPI_MISO = 13
SPI_SCK = 12

I2C_SDA = 8
I2C_SCL = 9

SD_CS= 10
SD_MOSI = 46
SD_MISO = 35
SD_SCK =45

TFT_CS = 1
TFT_DC =2
TFT_RST= 42
TFT_BL = 4


I2S_DOUT = 7
I2S_BCLK =6
I2S_LRC =5
I2C_DIN =15
AMP_SD =41


button1 = 38
button2 = 39
RT_SW = 18
RT_A =14
RT_B = 17

## font_Unispace = XglcdFont('Unispace12x24.c', 12, 24)   - I can import fonts like this Ill test this when I get the display


class System_Init:
    def __init__(self):
        self.sd_mounted = False
        self.i2s_initialized = False
        self.rtc_initialized = False
        self.display_initialized = False
        self.spi_initialized= False

        self.spi_tft = None
        self.spi_sd = None
        self.i2s = None

        self.display = None
        self.sd_card = None
        self.rtc = None
       

        #display configuartion
        self.display_width = 320
        self.display_height = 240
        self.display_rotation = 270
        
    def init_spi(self):
        print("Initializing SPI")

        try:
            self.spi_tft = SPI(2, baudrate=10000000, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
            self.spi_sd= SPI(1, baudrate=10000000,sck= SD_SCK, mosi = Pin(SD_MOSI), miso = Pin(SD_MISO))
            
            self.spi_initialized = True
            return True
        
        except Exception as e:
            print(f"Init failed {e}")
            self.spi_initialized =False
            return False
        

    def init_i2c_clock(self):
        print("Initializing I2c")

        try:
            i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)
            self.rtc = DS3231(i2c)
            print("I2c Clock Initalized")
            self.rtc_initialized= True

            # Scan for I2C devices
            devices = self.i2c.scan()
            print(f"Found {len(devices)} I2C device(s): {[hex(addr) for addr in devices]}")
        except Exception as e:
            print(f"Clock init failed {e}")
            self.rtc_initialized= False


    def init_display(self):
        print("Display init")
        try:
            self.display = Display(self.spi_tft,cs=Pin(TFT_CS),dc=Pin(TFT_DC),rst=Pin(TFT_RST),width=self.display_width,height=self.display_height,rotation=self.display_rotation) 

            # Set Backlight pin High
            Pin(TFT_BL, Pin.OUT).value(1)
            self.display.clear()
            self.display_initialized = True

            display.draw_text(100,50,"Display Init Success",0x001F) #drawing text for confirmation -will remove after testing
            
            return True
        except Exception as e:
            print(f"Display initialization failed: {e}")
            self.display_initialized = False
            return False
        

    def init_sdcard(self):
        print("Sd inititialization")

        try:
            self.sd_card = SDCard(self.spi_sd, cs=Pin(SD_CS),freq=20000000 )

            #have to check which freq it can run at later
            os.mount(self.sd_card, "/sd")
            print(files)    #for testing only
            print("Sucess")
            self.sd_mounted =True
            return True

        except Exception as e:
            print(f"Failure {e}")
            self.sd_mounted=  False

    def init_i2s(self):
        print("Initializing I2S")
        
        try:
            self.amp_en = Pin(AMP_SD, Pin.OUT)  #keeping this as output to control amp on/off
            self.amp_en.value(1) #high


            self.i2s = I2S(0, 
                           sck=Pin(I2S_BCLK), 
                           ws=Pin(I2S_LRC), 
                           sd=Pin(I2S_DOUT),
                           mode=I2S.TX, 
                           bits=16, 
                           format=I2S.MONO, 
                           rate=16000, 
                           ibuf=20000)
            
            self.i2s_initialized = True
            print("I2S initialized")
            return True
            
        except Exception as e:
            print(f"I2S failed {e}")
            self.i2s_initialized = False
            return False
            
    def run_all(self): #boot sequence
        self.init_spi()
        self.init_i2c_clock()
        self.init_display()
        self.init_sdcard()
        self.init_i2s()

class Controls():
    def __init__(self):
        self.btn1 = Pin(button1, Pin.IN, Pin.PULL_UP)
        self.btn2 = Pin(button2, Pin.IN, Pin.PULL_UP)

        self.pin_a = Pin(RT_A, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(RT_B, Pin.IN, Pin.PULL_UP)
        self.pin_sw = Pin(RT_SW, Pin.IN, Pin.PULL_UP)
        
        self.encoder_value = 1
        self.last_val_a = self.pin_a.value()
        print("Encoder pins configured")

    def read_encoder(self):
        current_val_a = self.pin_a.value()
        change_detected = False
        
        if current_val_a != self.last_val_a:
            # Determine direction
            if self.pin_b.value() != current_val_a:
                self.encoder_value += 1  # Clockwise
            else:
                self.encoder_value -= 1  # Counter-clockwise
            
         
            self.last_val_a = current_val_a
            change_detected = True
            
        return change_detected
    
    def button_pressed(self):
        if pin_Sw.value() == 0:
            return True
        return False

    def map_encoder_values(self, maxlimit):
        # This one line handles both the upper and lower bounds
        self.encoder_value = max(1, min(maxlimit, self.encoder_value))
        return self.encoder_value