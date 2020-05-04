init offset = 10
init python in game:
    import store.constants as constants

    over = False

    # resources
    fuel = constants.START_FUEL
    money = constants.START_MONEY
    food = constants.START_FOOD
    seeds = constants.START_SEEDS

    # time
    hour = 0
    day = 1

    # ship
    pos = 0
    shields = 0
    warp = 0

    # crops
    active_crop_id = -1
    crop_list = []
    crop_slots = constants.START_CROP_SLOTS
    for i in range(crop_slots):
        crop_list.append(None)

    class LocationException(Exception):
        pass

    class Location:
        def __init__(self, name, in_ship=False):
            self.name = name
            self.music = None
            self.bg = 'bg ' + name
            self.in_ship = in_ship

        def set_music(self, name, t):
            if t == 0:
                self.music = name
            else:
                self.music = '<loop %f>music/%s.ogg' % (t, name)

    SPACE_MUSIC_LOOP = 21.33

    loc_bridge = Location('bridge', True)
    loc_bridge.set_music('space', SPACE_MUSIC_LOOP)

    loc_power = Location('power', True)
    loc_power.set_music('space', SPACE_MUSIC_LOOP)

    loc_crops = Location('crops', True)
    loc_crops.set_music('space', SPACE_MUSIC_LOOP)

    location = None
    prev_location = None

    def set_location(new_location):
        if new_location is None:
            raise LocationException('Cannot have None location')

        global location, prev_location
        prev_location = location
        location = new_location
        new_music = prev_location is None or location.music != prev_location.music

        if location.music is not None and new_music:
            renpy.music.play(location.music)
        renpy.scene()
        renpy.show(location.bg)

    def update():
        update_move()
        global hour, day
        hour += 1
        while hour >= 24:
            day += 1
            hour -= 24

    def update_move():
        global fuel
        fuel -= constants.FUEL_IDLE
        if warp == 0:
            return

        global pos
        pos += constants.SPEED_WARP[warp]
        fuel -= constants.FUEL_RUNNING


label game_over_starve:
    hide screen info_display
    "Three days without food is as much as we can take. I'm the last survivor, but it won't be long until..."
    call game_over
    return


label game_over:
    scene bg game over with dissolve
    play music "<loop 27.0>music/game_over.ogg"
    show text "{size=60}GAME OVER" at truecenter with dissolve
    label game_over_loop:
        $renpy.pause(24 * 60 * 60)
        show text "{size=60}GAME OVER" at truecenter
        jump game_over_loop


label game_start:
    $game.set_location(game.loc_bridge)

    show screen ship_display
    while not game.over:
        $game.update()
        if game.location is game.loc_bridge:
            call menu_bridge
        elif game.location is game.loc_crops:
            call menu_crops
        elif game.location is game.loc_power:
            call menu_power
        elif game.location is None:
            $game.set_location(game.loc_bridge)
        else:
            $raise game.LocationException('Unknown location %s' % game.location.name)
        #call handle_events


label win_game:
    hide screen info_display
    hide screen ship_display

    stop ambient
    stop music fadeout 3

    $ning_in_crew = ning in crew.list
    if ning_in_crew:
        show ning happy at right
        N "We're... we're here! It's so beautiful."

    $klaara_in_crew = klaara in crew.list
    if klaara_in_crew:
        show klaara happy at left
        K "Indeed. Mission accomplished, sir."

    "I can hardly believe my eyes..."

    scene bg earth with irisout
    play music "<loop 43.2>music/earth.ogg"

    "Finally, we have arrived home."

    scene bg earth
    show text "{size=60}THE END" as end at top with dissolve
    show text "{size=40}THANK YOU FOR PLAYING!" as thanks at center with dissolve
    label win_game_loop:
        $renpy.pause(24 * 60 * 60)
        show text "{size=60}THE END" as end at top
        show text "{size=40}THANK YOU FOR PLAYING!" as thanks at center
        jump win_game_loop
