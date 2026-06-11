import lvgl as lv
import uasyncio

from pages.components import custom_button

from actions.play_from_flash import playWavFromFlash
from actions.play_from_sd import play_music_first_file



def build_music(parent, router):
    from context import songs_list as songs
    
    parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    parent.set_flex_align(lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
    parent.set_style_pad_row(20, lv.PART.MAIN)
    
    title = lv.label(parent)
    title.set_text("Music")
    title.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
    
    list_obj = lv.list(parent)
    list_obj.set_size(300, 200)
    list_obj.center()
    
    for song in songs:
        btn = list_obj.add_button(None, song["title"])
        btn.set_user_data(song["filename"])
        
    
    
    uasyncio.create_task(play_music_first_file())  # to start the music task immediately.
    # the play and pause is set by the context play event. It starts up as false. Gotta press play to start playback

    
def musicInput_handler(btn1, btn2, sw, cw, acw, router):
    import context
    if btn1:
        if context.play.is_set():
            context.play.clear() #sets the event to false to stop the music
        else:
            context.play.set()  #sets the event to false
    elif btn2:
        router.navigate_to("home")
        
    elif cw:
        if context.volume <100:
            context.volume= min(100, context.volume+2)
            print("Voume increased to:",context.volume)
        else:
            print("Volume change outside bound")
    elif acw:
        if context.volume > 0:
            context.volume = max(0,context.volume-2)
            print("Voume decreased to:",context.volume)
        else:
            print("Volume change outside bound")
            




