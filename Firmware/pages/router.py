import lvgl as lv
from pages.home import build_home, homeInput_handler
from pages.music import build_music,musicInput_handler
from pages.present import build_present,presentInput_handler
from pages.song import build_song, songInput_handler

class UIRouter:
    def __init__(self):
        self.scr = lv.screen_active()
        self.current_container = None
        
        self.active_input_handler = None
        self.active_progress_bar = None
        self.active_spinning_cd = None
        
        self.scr.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
        
        self.routes= {
            "home": build_home,
            "music": build_music,
            "present": build_present,
            "song" : build_song
            }
        
        self.input_routes= {
            "home" : homeInput_handler,
            "music" : musicInput_handler,
            "present":presentInput_handler,
            "song":songInput_handler
            
            }
        
    def navigate_to(self, route_name, **kwargs): #**kwargs is to wrap custom paramters for pages in a dict
        print(f"Switching viiew to  {route_name}")
        
        self.active_progress_bar = None
        self.active_spinning_cd =None
        if self.current_container:
            self.current_container.delete()
            
        self.current_container = lv.obj(self.scr)
        self.current_container.set_size(320,240)
        self.current_container.set_style_bg_opa(lv.OPA.TRANSP, lv.PART.MAIN)
        self.current_container.set_style_border_width(0, lv.PART.MAIN)
        
        
        if route_name in self.routes:
            self.routes[route_name](self.current_container, self, **kwargs)
            self.active_input_handler = self.input_routes[route_name]
            
        else:
            print("Routing error: Key mismatch")
            
    def process_input(self, btn1= False, btn2= False,sw =False,cw= False,acw= False):
        if self.active_input_handler:
            self.active_input_handler(btn1, btn2,sw, cw, acw,self)
    
            



