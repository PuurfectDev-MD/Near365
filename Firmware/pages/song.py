import lvgl as lv
def build_song(parent, router, songtitle="unknown", time="0:00"):
    parent.set_style_bg_color(lv.color_hex(0xFFFFFF),0)


    button_row = lv.obj(parent)
    button_row.align(lv.ALIGN.BOTTOM_MID, 0, -5)
    button_row.set_flex_align(
        lv.FLEX_ALIGN.SPACE_EVENLY, 
        lv.FLEX_ALIGN.CENTER, 
        lv.FLEX_ALIGN.CENTER
    )
    button_row.set_size(300, 60)

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

    needle_base = lv.obj(parent)
    needle_base.set_size(24, 24)
    needle_base.set_style_radius(32767, 0)
    needle_base.set_style_bg_color(lv.color_hex(0x888888), 0)
    needle_base.align(lv.ALIGN.TOP_LEFT, 10, 112)

    parent.update_layout()

    pivot_x = needle_base.get_x() + 12
    pivot_y = needle_base.get_y() + 12

    # 3. Initialize the line on the parent screen
    needle_rod = lv.line(parent)
    needle_rod.set_style_line_color(lv.color_hex(0xCCCCCC), 0)

    needle_rod.set_style_line_width(4, 0) 

    rod_points = [
        {"x": pivot_x, "y": pivot_y},        # Point 1: Center of Pivot Base
        {"x": pivot_x + 90, "y": pivot_y - 85}  # Point 2: Tip where needle rests
    ]

    needle_rod.set_points(rod_points, 2)



    music_area = lv.obj(parent)
    music_area.align(lv.ALIGN.RIGHT_MID,-10, -40)
    music_area.set_style_bg_color(lv.color_hex(0xE8ECEF),0)
    music_area.set_size(150,150)

    music_area.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    music_area.set_flex_align(
        lv.FLEX_ALIGN.START, 
        lv.FLEX_ALIGN.START, 
        lv.FLEX_ALIGN.START
    )


    context = lv.label(music_area)
    context.set_text("Now playing")

    song = lv.obj(music_area)
    song.set_size(120, 55)
    song.set_style_bg_color(lv.color_hex(0xE7ECEF),0)

    song_name = lv.label(song)
    song_name.set_text(f"{songtitle}")
    song_name.set_style_text_color(lv.color_hex(0x333333), 0)


    duration_obj = lv.obj(music_area)
    duration_obj.add_flag(lv.obj.FLAG.FLOATING)
    duration_obj.set_size(70, 60)
    duration_obj.align(lv.ALIGN.BOTTOM_RIGHT,10,20)
    duration_obj.set_style_bg_color(lv.color_hex(0xE7ECEF),0)


    duration = lv.label(duration_obj)
    duration.set_text(f"{duration}")
    duration.set_style_text_color(lv.color_hex(0x333333), 0)
    duration_obj.set_style_bg_opa(0, 0)    
    duration_obj.set_style_border_opa(0, 0)



def songInput_handler(btn1, btn2, sw, cw, acw, router):
    import context
    if btn1:
        router.navigate_to("music")
        
    elif btn2:
        if context.play.is_set():
            context.play.clear() #sets the event to false to stop the music
        else:
            context.play.set()  #sets the event to false


