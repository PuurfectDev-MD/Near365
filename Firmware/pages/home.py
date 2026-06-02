import lvgl as lv
from pages.components import custom_button

def build_home(parent, router):
    parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    parent.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
    parent.set_style_pad_row(15, lv.PART.MAIN)
    
    title = lv.label(parent)
    title.set_text("HOME")
    title.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
    
    custom_button(parent, "Music", lambda e: router.navigate_to("music"))
    custom_button(parent, "Settings", lambda e: router.navigate_to("settings"))
    
    
def homeInput_handler(btn1, btn2,router):
    if btn1:
        router.navigate_to("music")
    elif btn2:
        router.navigate_to("music")
        
