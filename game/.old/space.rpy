transform shipmovein(ship_pos):
    xanchor 0.5 yanchor 0.5 ypos 0.5 xpos -0.1
    #linear ship_pos * 10 xpos ship_pos
    easein 12 xpos ship_pos

label show_space(ship_pos):
    scene bg space at horizontal_loop with irisin
    show ship at shipmovein(ship_pos)
    return
