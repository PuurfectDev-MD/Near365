import lvgl as lv

def build_present(parent, router):
    from context import today_present
    
    today_message = today_present.get("message", "No message idk why. something went wrong")
    artist = today_present.get("artist", "unknown")
    title = today_present.get("audio", "unknown")
    parent.set_size(320, 240)
    

    
    main_container = lv.obj(parent)
    main_container.set_size(300, 120)
    main_container.align(lv.ALIGN.TOP_MID, 0, 20)
    message = lv.label(main_container)
    message.set_size(250,120)
    message.set_text(f"{today_message}")

    music_container = lv.obj(parent)
    music_container.set_size(300, 50) 
    music_container.align(lv.ALIGN.BOTTOM_MID, 0, -10) 

    music_container.set_style_bg_color(lv.color_hex(0x444444), 0)
    music_container.set_style_bg_opa(lv.OPA.COVER, 0)
    music_container.set_style_text_color(lv.color_hex(0xFFFFFF), 0)


    music_container.set_style_pad_all(0, 0)

    logo_label = lv.label(music_container)
    logo_label.set_text(lv.SYMBOL.AUDIO)

    logo_label.align(lv.ALIGN.LEFT_MID, 15, 0) 

    label_title = lv.label(music_container)
    label_title.set_text(f"{title}")
    label_title.align(lv.ALIGN.RIGHT_MID, -15, -10) 

    label_artist = lv.label(music_container)
    label_artist.set_text(f"{artist}")
    label_artist.align(lv.ALIGN.RIGHT_MID, -15, 10)

    label_artist.set_style_text_opa(lv.OPA._60, 0)
    
    
#     parent.set_flex_flow(lv.FLEX_FLOW.COLUMN)
#     parent.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
#     parent.set_style_pad_row(15, lv.PART.MAIN)
#     
#     main_message = lv.container(parent)
#     main_message.set_flex_flow(lv.FLEX_FLOW.COLUMN)
#     main_message.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
#     
#     music_container = lv.container(parent)
#     music_container.set_flex_flow(lv.FLEX_FLOW.ROW)
#     music_container.set_flex_align(lv.FLEX_ALIGN.BOTTOM, lv.FLEX_ALIGN.CENTER,lv.FLEX_ALIGN.CENTER)
#     
#     music_icon = lv.label(music_container)
#     music_icon.set_text(lv.SYMBOL.MUSIC)
#     
#     music_label = lv.label(music_container)
#     music_label.set_text("Music title")
#     
#     main_message_label = lv.label(main_message)
#     main_message_label.set_text("This is the main message")
#     main_message_label.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN)
#     print("The page is built fully")


    
def presentInput_handler(btn1, btn2, sw, cw, acw, router):
    if btn1:
        router.navigate_to("home")
    elif btn2:
        router.navigate_to("music")

