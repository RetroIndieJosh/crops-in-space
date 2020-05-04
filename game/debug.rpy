init python in startup:
    # turn off all debug features if we're not in debug mode
    def init_debug():
        if config.developer:
            return
        persistent.skip_intro = False
        persistent.skip_battle_intro = False
        persistent.auto_name = False
        persistent.debug_options = False

label menu_debug:
    menu:
        "DEBUG MENU"

        "Advance 10 LY":
            $game.pos += 10
        "Advance 10 hours":
            $game.hour += 10
        "Go to Earth":
            $game.pos = constants.EARTH_DISTANCE
        "Test win":
            call win_game
        "Seed crop 0 (overwrite current crop)":
            $game.crop_list[0] = Crop('turnip')
        "Grow crop 0 (if able)":
            $game.crop_list[0].grow()

        #"Test starve":
            #call game_over_starve
        #"Test combat":
            #call set_engine_level(0)
            #$cur_enemy = enemy_list[0]
            #$enemy_list.remove(cur_enemy)
            #call battle_start
        #"Test planet":
            #$cur_planet = planet_list[0]
            #call planet_land_animate
        #"Test crew leave":
            #$crew_list[0].morale = Constants.MORALE_LEAVE
    return


label wait(hr=0):
    if hr <= 0:
        call prompt_amount("How long should I wait (hours)?")
        if _return > Constants.MAX_WAIT_HR:
            "I can't wait around for more than [Constants.MAX_WAIT_HR] hours."
            jump wait
        $hr = _return
    python:
        game_time.add_hours(hr)
    return
