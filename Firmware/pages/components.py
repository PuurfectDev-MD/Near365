import lvgl as lv
_btn_style = None


def _get_btn_style():
    global _btn_style
    if _btn_style is None:
        _btn_style = lv.style_t()
        _btn_style.init()
        _btn_style.set_radius(6)
        _btn_style.set_bg_opa(lv.OPA.COVER)
        _btn_style.set_bg_color(lv.palette_main(lv.PALETTE.BLUE))
        _btn_style.set_text_color(lv.color_white())
    return _btn_style

def custom_button(parent, text, callback, width=140, height=45):
    btn = lv.button(parent)
    btn.set_size(width,height)
    btn.add_style(_get_btn_style(), lv.PART.MAIN)
    
    
    lbl = lv.label(btn)
    lbl.set_text(text)
    lbl.center()
    
    if callback:
        btn.add_event_cb(callback, lv.EVENT.CLICKED, None)
        
    return btn

