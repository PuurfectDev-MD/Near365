# from ds3231 import DS3231
from machine import I2S, Pin, SPI
import time
import lvgl as lv
import ili9xxx
# master_file = master.json #file on sd card with all info   - stored on sd card
# daily_file = daily.json #file info extracted on this for today (one day) -stored on esp flash
from sdcard import SDCard
import os


WIFI_SSID = ""
WIFI_PASS = ""



SPI_MOSI = 11
SPI_MISO = 13
SPI_SCK = 12


I2C_SDA = 8
I2C_SCL = 9

SD_CS= 10
SD_MOSI = 9
SD_MISO = 8
SD_SCK =3

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
        self.display_rotation = 3
        
    def init_spi(self):
        print("Initializing SPI")

        try:
            self.spi_tft = SPI(2, baudrate=20000000, sck=Pin(SPI_SCK), mosi=Pin(SPI_MOSI), miso=Pin(SPI_MISO))
            self.spi_sd= SPI(1, baudrate=4000000,sck=Pin(SD_SCK), mosi = Pin(SD_MOSI), miso = Pin(SD_MISO))
            return True
        
        except Exception as e:
            print(f"Init failed {e}")
            return False
        


    def init_display(self):
        print("Display init")
        try:
            Pin(TFT_BL, Pin.OUT).value(1)
            
            if lv.is_initialized():
                print("LVGL was already running from a previous state. Cleaning up...")
                lv.deinit()
                
            lv.init()
            print("Running LVGL %d.%d" % (lv.version_major(), lv.version_minor() )  )

            self.display = ili9xxx.Ili9341(spi=self.spi_tft,
                            dc=TFT_DC,
                            cs=TFT_CS,
                            rst=TFT_RST,
                            rot=self.display_rotation,
                        )
                        
            print("The tft has been initialized natively")

            return True
        except Exception as e:
            print(f"Display initialization failed: {e}")
            return False
        

    def init_sdcard(self):
        print("Sd inititialization")

        try:
            self.sd_card = SDCard(self.spi_sd, cs=Pin(SD_CS))
            vfs = os.VfsFat(self.sd_card)
            os.mount(self.sd_card, "/sd")
            print(os.listdir("/sd"))   
            print("Sucess on mounting sd card")
            return True

        except Exception as e:
            print(f"Failure {e}")
            self.sd_mounted=  False

    def init_i2s(self):
        print("Initializing I2S")
        
        try:
            self.amp_en = Pin(AMP_SD, Pin.OUT)
            self.amp_en.value(1) 


            self.i2s = I2S(0, 
                           sck=Pin(I2S_BCLK), 
                           ws=Pin(I2S_LRC), 
                           sd=Pin(I2S_DOUT),
                           mode=I2S.TX, 
                           bits=16, 
                           format=I2S.MONO, 
                           rate=22050, 
                           ibuf=20000)
            
            print("I2S initialized")
            return True
            
        except Exception as e:
            print(f"I2S failed {e}")
            self.i2s_initialized = False
            return False
            
    def run_all(self): #boot sequence
        
        self.spi_initialized= self.init_spi()
        self.i2s_initialized = self.init_i2s()
        
        if not lv.is_initialized():
            lv.init()
            
        self.display_initialized = self.init_display()
        self.sd_mounted = self.init_sdcard()




class Controls():
    def __init__(self):
        self.btn1 = Pin(button1, Pin.IN, Pin.PULL_UP)
        self.btn2 = Pin(button2, Pin.IN, Pin.PULL_UP)

        self.pin_a = Pin(RT_A, Pin.IN, Pin.PULL_UP)
        self.pin_b = Pin(RT_B, Pin.IN, Pin.PULL_UP)
        self.pin_sw = Pin(RT_SW, Pin.IN, Pin.PULL_UP)
        
        self.encoder_value = 0
        
        val_a = self.pin_a.value()
        val_b = self.pin_b.value()
        self.current_state = (val_a << 1) | val_b
        self.last_state = self.current_state

        self.state_table = [
            [0,  1, -1,  0],  
            [-1, 0,  0,  1],  
            [1,  0,  0, -1], 
            [0, -1,  1,  0]   
        ]
        
    
        self.sub_step_counter = 0 
        
        print("Hardware pins configured with State Machine Matrix")

    def read_encoder(self):
        val_a = self.pin_a.value()
        val_b = self.pin_b.value()
        

        self.current_state = (val_a << 1) | val_b
        
        change_detected = False
        
        if self.current_state != self.last_state:
            movement = self.state_table[self.last_state][self.current_state]
            
            if movement != 0:
                self.sub_step_counter += movement
                
                if abs(self.sub_step_counter) >= 2: 
                    if self.sub_step_counter > 0:
                        self.encoder_value += 1
                    else:
                        self.encoder_value -= 1
                    
                    self.sub_step_counter = 0 
                    change_detected = True
            
            self.last_state = self.current_state
            
        return change_detected

    def is_en_sw_pressed(self): return self.pin_sw.value() == 0
    def is_btn1_pressed(self): return self.btn1.value() == 0
    def is_btn2_pressed(self): return self.btn2.value() == 0
