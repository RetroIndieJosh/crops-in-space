init python:
    narrator = Character(what_italic=True)

style block1_multiple2_say_window:
    xpos 0.5
    xsize 1.0

style block2_multiple2_say_window:
    xpos 0.5
    xsize 0.5
    background None

label name_player:
    if persistent.auto_name:
        $name = "Sarge"
        jump naming_done

    python:
        name = renpy.input("Enter your name:", default="")
        name = name.strip()
        if not name:
            name = "Sarge"

    menu:
        "Did I get that right, [name]?"
        "Yes":
            jump naming_done
        "No":
            jump name_player

    label naming_done:
        define player = Character('[name]')
        return
