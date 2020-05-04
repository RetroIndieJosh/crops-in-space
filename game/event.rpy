label handle_events:
    python:
        print("%d events in list" % len(cur_event))
        while len(cur_event) > 0:
            renpy.call('handle_event', cur_event.pop())
    return


label handle_event(e):
    $print('handle event %s' % e)
    if e == ShipEvent.ARRIVED_EARTH:
        call win_game
    elif e == ShipEvent.LOW_FUEL:
        if station_engine is not None:
            call show_crew(station_engine, 'upset')
            $renpy.say(station_engine, "Sir, we're running low on fuel. We should convert food or stop at a planet soon.")
            call hide_crew(station_engine)
        else:
            "Ship Computer" "Warning! Low fuel supply."
    elif e == ShipEvent.NO_FUEL:
        play sound "sound/engine_die.wav"
        "The ship creaks as the engines run out of fuel."
        call set_engine_level(0)
    elif e == ShipEvent.APPROACHING_PLANET:
        $dist = distance_to(near_planet.name)
        "We're getting near a planet! [dist] LY to go."
    elif e == ShipEvent.PASSED_PLANET:
        "We passed the planet."
        $near_planet = None
    elif e == ShipEvent.LANDING_PLANET:
        call planet_land
    elif e == ShipEvent.ENEMY_ENCOUNTER:
        call battle_start
    elif e == ShipEvent.SHIELDS_CHARGED:
        "The shields are fully charged."

    return
