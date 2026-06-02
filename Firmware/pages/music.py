import lvgl as lv
from pages.components import custom_button

def build_music(parent, router):
    parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    parent.set_flex_align(lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
    parent.set_style_pad_row(20, lv.PART.MAIN)
    
    title = lv.label(parent)
    title.set_text("Music")
    title.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
    
    
    custom_button(parent, "Back Home", lambda e: router.navigate_to("home"))
    
    
    
def musicInput_handler(btn1, btn2,router):
    if btn1:
        router.navigate_to("home")
    elif btn2:
        router.navigate_to("home")
        




