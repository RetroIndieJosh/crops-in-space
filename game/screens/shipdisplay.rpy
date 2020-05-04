init python:
    import store.constants as constants
    import store.game as game

    def get_ship_pos():
        percent = float(game.pos) / constants.EARTH_DISTANCE
        return percent * 0.75 + 0.1

screen ship_display():
    frame:
        xysize (1920, 50)
        add "spr earth.png" xalign 0.9 yalign 0.5
        add "spr ship.png" xalign get_ship_pos() yalign 0.5
