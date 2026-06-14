import lvgl as lv
from pages.components import custom_button
import random
import context
def build_home(parent, router):
    parent.set_style_bg_color(lv.color_hex(0xFFFFFF),0)
    parent.set_scroll_dir(lv.DIR.NONE)
    icons_menu = lv.obj(parent)
    icons_menu.set_size(200, 50)
    icons_menu.set_style_bg_color(lv.color_hex(0xDDDDDD),0)
    icons_menu.set_flex_align(
            lv.FLEX_ALIGN.SPACE_EVENLY, 
            lv.FLEX_ALIGN.CENTER, 
            lv.FLEX_ALIGN.CENTER
        )
    icons_menu.align(lv.ALIGN.TOP_RIGHT,0,0)

    icons_menu.set_scroll_dir(lv.DIR.NONE)


    wifi = lv.label(icons_menu)
    wifi.set_text(lv.SYMBOL.WIFI)
    wifi.set_style_text_color(lv.color_hex(0xEB1A1A), 0) #red


    sd_logo = lv.label(icons_menu)
    sd_logo.set_text(lv.SYMBOL.SD_CARD)
    sd_logo.set_style_text_color(lv.color_hex(0xEB1A1A), 0)


    gift_label = lv.line(icons_menu)
    gift_label.set_size(16, 16)

    gift_points = [
        {"x": 1, "y": 5}, {"x": 15, "y": 5},  
        {"x": 15, "y": 7}, {"x": 1, "y": 7},  
        {"x": 1, "y": 5},                      
        {"x": 3, "y": 7}, {"x": 3, "y": 15},  
        {"x": 13, "y": 15}, {"x": 13, "y": 7}, 
        {"x": 8, "y": 7}, {"x": 8, "y": 15},  
        {"x": 8, "y": 5}, {"x": 5, "y": 1},   
        {"x": 8, "y": 1}, {"x": 8, "y": 5},  
        {"x": 11, "y": 1}, {"x": 8, "y": 1}    
    ]

    gift_label.set_points(gift_points, len(gift_points))
    gift_label.set_style_line_color(lv.color_hex(0xEB1A1A), 0)
    gift_label.set_style_line_width(2, 0)


    clock_label = lv.line(icons_menu)
    clock_label.set_size(20, 20)

    clock_points = [
        {"x": 6, "y": 2},  {"x": 14, "y": 2},   
        {"x": 18, "y": 6}, {"x": 18, "y": 14},  
        {"x": 14, "y": 18}, {"x": 6, "y": 18},
        {"x": 2, "y": 14}, {"x": 2, "y": 6},   
        {"x": 6, "y": 2},                      
        {"x": 10, "y": 10},                     
        {"x": 10, "y": 5},                     
        {"x": 10, "y": 10},                     
        {"x": 14, "y": 10}                     
    ]

    clock_label.set_points(clock_points, len(clock_points))
    clock_label.set_style_line_color(lv.color_hex(0xEB1A1A), 0)
    clock_label.set_style_line_width(2, 0)
    
    context.home_logo_objs = [wifi,sd_logo,gift_label,clock_label]  #saving to update it on main file


    left_col = lv.obj(parent)
    left_col.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    left_col.set_flex_align(lv.FLEX_ALIGN.SPACE_AROUND, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    left_col.align(lv.ALIGN.LEFT_MID, -20, 0)
    left_col.set_size(75,75)
    left_col.set_scroll_dir(lv.DIR.NONE)

    left_arrow = lv.label(left_col)
    left_arrow.set_text(lv.SYMBOL.LEFT)

    left_text = lv.label(left_col)
    left_text.set_text("Music")

    right_col = lv.obj(parent)
    right_col.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    right_col.set_flex_align(lv.FLEX_ALIGN.SPACE_AROUND, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    right_col.align(lv.ALIGN.RIGHT_MID, 17, 0)
    right_col.set_size(75,75)
    right_col.set_scroll_dir(lv.DIR.NONE)

    right_arrow = lv.label(right_col)
    right_arrow.set_text(lv.SYMBOL.RIGHT)


    right_text = lv.label(right_col)
    right_text.set_text("Present")




    bar_container = lv.obj(parent)
    bar_container.set_size(250, 100)
    bar_container.center()
    bar_container.set_flex_flow(lv.FLEX_FLOW.ROW)
    bar_container.set_flex_align(lv.FLEX_ALIGN.SPACE_BETWEEN, lv.FLEX_ALIGN.END, lv.FLEX_ALIGN.END)
    bar_container.align(lv.ALIGN.BOTTOM_MID,0,20)
    bar_container.set_style_bg_opa(lv.OPA.TRANSP, 0)
    bar_container.set_style_border_width(0, 0)
    
    router.active_anim_bars = bars = []
    
    for i in range(9):
        bar = lv.obj(bar_container)
        bar.set_size(20, random.randint(30, 80)) 
        bar.set_style_bg_color(lv.color_hex(0xFFFFFF), 0)  
        bar.set_style_border_width(0, 0)           
        bar.set_style_radius(0, 0)
        
        bar.set_style_bg_color(lv.color_hex(0xA8A9AD), 0)      # Top color 
        bar.set_style_bg_grad_color(lv.color_hex(0xFAF7F7), 0) # Bottom color 
        
        # Tell LVGL to draw the gradient vertically (Top to Bottom)
        bar.set_style_bg_grad_dir(lv.GRAD_DIR.VER, 0)
        bars.append(bar)

    bar_container.set_scroll_dir(lv.DIR.NONE)

    
    
def homeInput_handler(btn1, btn2, sw, cw, acw,router):
    import context
    if btn1:
        router.navigate_to("music")
    elif btn2:
        router.navigate_to("present")
        
    elif sw:
        if context.play.is_set():
            context.play.clear() #sets the event to false to stop the music
        else:
            context.play.set()  #sets the event to false
        


