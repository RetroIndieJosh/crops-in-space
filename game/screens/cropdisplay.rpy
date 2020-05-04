init python:
    def set_active_crop(i):
        print("Active crop: #%d" % i)
        game.active_crop_id = i

screen crop_display():
    vbox:
        xcenter 0.5 ycenter 0.5
        grid len(game.crop_list) 1:
            for i in range(game.crop_slots):
                frame:
                    if game.crop_list[i] is None:
                        add "spr dirt"
                    else:
                        imagebutton auto game.crop_list[i].get_image() + " %s" action [Function(set_active_crop, i), Return()]
        frame:
            textbutton "Done" action Return()
