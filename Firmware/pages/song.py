import lvgl as lv
import uasyncio

from actions.play_from_sd import play_music_from_file

def build_song(parent, router, songtitle="unknown", time="0:00"):
    import context
    parent.set_style_bg_color(lv.color_hex(0xFFFFFF),0)


    button_row = lv.obj(parent)
    button_row.align(lv.ALIGN.BOTTOM_MID, 0, -5)
    button_row.set_flex_align(
        lv.FLEX_ALIGN.SPACE_EVENLY, 
        lv.FLEX_ALIGN.CENTER, 
        lv.FLEX_ALIGN.CENTER
    )
    button_row.set_size(300, 50)

    forward = lv.label(button_row)
    forward.set_text(lv.SYMBOL.NEXT)

    play = lv.label(button_row)
    play.set_text(lv.SYMBOL.PLAY)

    backward= lv.label(button_row)
    backward.set_text(lv.SYMBOL.PREV)

    cd = lv.obj(parent)
    cd.set_size(120,120)
    cd.align(lv.ALIGN.LEFT_MID, 3, -45)

    cd.set_style_bg_color(lv.color_hex(0x2A2A2A),0)
    cd.set_style_border_width(3,0)
    cd.set_style_border_color(lv.color_hex(0x1AB111), 0)
    cd.set_style_radius(32767, 0)
    
    cd.set_style_transform_pivot_x(60, 0)
    cd.set_style_transform_pivot_y(60, 0)
    
    
    
    dot_positions = [
    (-35, -20),  # Upper left speckle
    (25, -35),   # Top right speckle
    (-20, 30),   # Bottom left speckle
    (40, 15),    # Outer right speckle
    (-45, 5),    # Deep left speckle
    (15, 40)     # Bottom right speckle
]

    for x_offset, y_offset in dot_positions:
        dot = lv.obj(cd)
        dot.set_size(4, 4) 
        dot.set_style_radius(32767, 0) 
        dot.set_style_bg_color(lv.color_hex(0x888888), 0)
        dot.set_style_border_width(0, 0)
        dot.align(lv.ALIGN.CENTER, x_offset, y_offset)
        
        
    hole0 = lv.obj(cd)
    hole0.set_size(60,60)
    hole0.set_style_radius(32767, 0)
    hole0.center()
    hole0.set_style_bg_color(lv.color_hex(0x303234),0)

    hole = lv.obj(hole0)
    hole.set_size(50,50)
    hole.set_style_radius(32767, 0)
    hole.center()
    hole.set_style_bg_color(lv.color_hex(0xFFFFFF),0)

    hole2 = lv.obj(hole)
    hole2.set_size(30,30)
    hole2.set_style_radius(32767, 0)
    hole2.center()
    hole2.set_style_bg_color(lv.color_hex(0xFF0000),0)




    music_area = lv.obj(parent)
    music_area.align(lv.ALIGN.RIGHT_MID,-10, -40)
    music_area.set_style_bg_color(lv.color_hex(0xE8ECEF),0)
    music_area.set_size(150,150)
    
    music_area.set_scroll_dir(lv.DIR.NONE)
    music_area.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    music_area.set_flex_align(
        lv.FLEX_ALIGN.START, 
        lv.FLEX_ALIGN.START, 
        lv.FLEX_ALIGN.START
    )


    context_text = lv.label(music_area)
    context_text.set_text("Now playing")

    song = lv.obj(music_area)
    song.set_size(120, 55)
    song.set_style_bg_color(lv.color_hex(0xE7ECEF),0)

    song_name = lv.label(song)
    song_name.set_width(110)
    song_name.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
    song_name.set_style_text_color(lv.color_hex(0x333333), 0)
    song_name.set_text(f"{songtitle}")
    
    context.playing_title_obj = song_name


    duration_obj = lv.obj(music_area)
    duration_obj.add_flag(lv.obj.FLAG.FLOATING)
    duration_obj.set_size(70, 60)
    duration_obj.align(lv.ALIGN.BOTTOM_RIGHT,10,20)
    duration_obj.set_style_bg_color(lv.color_hex(0xE7ECEF),0)


    duration = lv.label(duration_obj)
    duration.set_text(f"{time}")
    duration.set_style_text_color(lv.color_hex(0x333333), 0)
    duration_obj.set_style_bg_opa(0, 0)    
    duration_obj.set_style_border_opa(0, 0)
    duration_obj.set_scroll_dir(lv.DIR.NONE)
    
    context.playing_time_obj = duration
        
    progress_bar = lv.bar(parent)
    progress_bar.set_size(250, 12)  
    progress_bar.align(lv.ALIGN.BOTTOM_MID, 0, -63)
    progress_bar.set_range(0, 100)      
    progress_bar.set_value(0, 0)

    progress_bar.set_style_bg_color(lv.color_hex(0xDDDDDD), lv.PART.MAIN) 
    progress_bar.set_style_bg_color(lv.color_hex(0x1AB111), lv.PART.INDICATOR)
    
    router.active_progress_bar = progress_bar  #to update this outside this fucn
    router.active_spinning_cd = cd  #same


def songInput_handler(btn1, btn2, sw, cw, acw, router):
    import context
    if btn1:
        to_play_index = context.now_playing_index -1 #backward
        if to_play_index < 0:
            to_play_index = len(context.songs_list)-1 #last song on the list
        filename = f"{context.songs_list[to_play_index]["title"]}.wav"
        
               
        context.playing_title_obj.set_text(f"{filename[:-4]}")
        context.playing_time_obj.set_text(f"idk")
               
        context.playing_title_obj.set_text(f"{filename[:-4]}")
        context.playing_time_obj.set_text(f"idk")
        
        context.song_focused_index = to_play_index
        context.now_playing_index = to_play_index
        
        if context.audio_task:
            context.audio_task.cancel()
        
        context.play.set()
        context.audio_task = uasyncio.create_task(play_music_from_file(filename))
        
    elif btn2:
        to_play_index = context.now_playing_index +1  #forward
        if to_play_index > (len(context.songs_list)-1):
            to_play_index = 0 # first song on the list
        filename = f"{context.songs_list[to_play_index]['title']}.wav"
        
        context.playing_title_obj.set_text(f"{filename[:-4]}")
        context.playing_time_obj.set_text(f"idk")
        
        context.song_focused_index = to_play_index
        context.now_playing_index = to_play_index
        
        if context.audio_task:
            context.audio_task.cancel()
        
        context.play.set()
        context.audio_task=uasyncio.create_task(play_music_from_file(filename))
        
        
    elif sw:
        if context.play.is_set():
            context.play.clear() #sets the event to false to stop the music
        else:
            context.play.set()  #sets the event to false
            
    elif cw or acw:
        print("Going back to the music list")
        router.navigate_to("music")
        




