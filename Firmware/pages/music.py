import lvgl as lv
import uasyncio

from pages.components import custom_button

from actions.play_from_flash import playWavFromFlash
from actions.play_from_sd import play_music_from_file


def build_music(parent, router):
    import context
    from context import songs_list as songs
    
    context.music_list_objs = []
    
    parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    parent.set_flex_align(lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
    parent.set_style_pad_row(20, lv.PART.MAIN)
    
    parent.set_scroll_dir(lv.DIR.NONE)
    
    title = lv.label(parent)
    title.set_text("Music")
    title.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
    
    list_obj = lv.list(parent)
    list_obj.set_style_bg_color(lv.color_hex(0x000000), lv.PART.MAIN)
    list_obj.set_size(310, 170)
    list_obj.center()
    
    focus_style = lv.style_t()
    focus_style.init()
    focus_style.set_bg_color(lv.color_hex(0x444444))
    focus_style.set_bg_opa(lv.OPA.COVER)
    focus_style.set_text_color(lv.color_hex(0xFFFFFF))
    
    for song in songs:
        btn = list_obj.add_button(None, song["title"])
        btn.add_style(focus_style, lv.PART.MAIN | lv.STATE.FOCUSED)
        context.music_list_objs.append(btn)
        
    button_row = lv.obj(parent)
    button_row.align(lv.ALIGN.BOTTOM_MID, 0, -35)
    button_row.set_scroll_dir(lv.DIR.NONE)
    button_row.set_flex_align(
        lv.FLEX_ALIGN.SPACE_EVENLY, 
        lv.FLEX_ALIGN.CENTER, 
        lv.FLEX_ALIGN.CENTER
    )
    button_row.set_size(300, 50)


    play = lv.label(button_row)
    play.set_text(lv.SYMBOL.PLAY)


    context.music_list_objs[context.song_focused_index].add_state(lv.STATE.FOCUSED)
        
    print("Music page is built fully")
    
def musicInput_handler(btn1, btn2, sw, cw, acw, router):
    import context
    if btn1:
        router.navigate_to("home")

        
    elif btn2:
        if context.now_playing_index == -1:
            playing_song = "No song playing at the moment"
        else:
            playing_song = context.songs_list[context.now_playing_index]["title"]
        router.navigate_to("song", songtitle =playing_song, time="5:00") # have to set up time later
       
#         if context.play.is_set():
#             context.play.clear() #sets the event to false to stop the music
#         else:
#             context.play.set()  #sets the event to false
    
    elif cw or acw:
        old_btn = context.music_list_objs[context.song_focused_index]
        old_btn.remove_state(lv.STATE.FOCUSED)
        
        if cw:
            if context.song_focused_index < (len(context.music_list_objs)-1):
                context.song_focused_index +=1
        elif acw:
            if context.song_focused_index >0:
                context.song_focused_index -=1
                
        new_btn = context.music_list_objs[context.song_focused_index]
        new_btn.add_state(lv.STATE.FOCUSED)
        new_btn.scroll_to_view(True)
                
    elif sw:
        print("To play another song now")
        selected_song = context.music_list_objs[context.song_focused_index]
        
        song = context.songs_list[context.song_focused_index]
        filename = song["filename"]
        
        if context.audio_task is not None:
            context.audio_task.cancel()
            
        print("Ended previous song. Starting a new task")
        context.play.set()
        print(f"Playing music file in {filename}")
        context.now_playing_index= context.song_focused_index
        print("Currently playing song:", context.now_playing_index)
        context.audio_task = uasyncio.create_task(play_music_from_file(filename))
       
        
#     elif cw:
#         if context.volume <100:
#             context.volume= min(100, context.volume+2)
#             print("Voume increased to:",context.volume)
#         else:
#             print("Volume change outside bound")
#     elif acw:
#         if context.volume > 0:
#             context.volume = max(0,context.volume-2)
#             print("Voume decreased to:",context.volume)
#         else:
#             print("Volume change outside bound")
#

      








