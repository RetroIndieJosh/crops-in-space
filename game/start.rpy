init python in startup:
    import store.constants as constants

    def init_audio():
        renpy.music.register_channel( "ambient", "sfx", True, tight=True)


init python:
    import store.game as game
    import store.startup as startup

    startup.init_audio()

    def update_time():
        renpy.show_screen("time_display", cur_time)


label start:
    #call intro_scene
    #show screen info_display with dissolve
    call game_start
    return


label prompt_amount(message):
    label retry_prompt_amount:
        python:
            success = True
            try:
                amount = int(renpy.input( message ))
                if amount < 0:
                    success = False
            except ValueError:
                success = False
        if not success:
            "Please enter a valid positive number (or zero)."
            jump retry_prompt_amount
    return amount


label assign_station(crew, station):
    call remove_from_stations(crew)
    python:
        prev_crew = None
        affinity = 0
        crew.resting = False
        if station == 'shields':
            affinity = crew.shields
            prev_crew = station_shields
            station_shields = crew
        elif station == 'engines':
            affinity = crew.engine
            prev_crew = station_engine
            station_engine = crew
        elif station == 'crops':
            affinity = crew.crops
            prev_crew = station_crops
            station_crops = crew

    if affinity > 0:
        call show_crew(crew, 'happy')
        $response = "Right away, sir! I'm glad to work %s." % station
    elif affinity < 0:
        call show_crew(crew, 'upset')
        $response = "Not my forte, but I'll get on %s." % station
    else:
        $response = "Okay, I'll get on %s." % station

    if prev_crew is not None:
        $response += " I'll let %s know that I'm replacing her." % prev_crew.name.title()

    $renpy.say(crew, response)
    return


label speak_to(crew):
    call show_crew(crew)

    $renpy.say(crew, crew.greeting)
    menu:

        "How are you doing?":
            if crew.morale <= -5:
                call show_crew(crew, 'upset')
                $renpy.say(crew, crew.morale_msg_bad)
            elif crew.morale >= 5:
                call show_crew(crew, 'happy')
                $renpy.say(crew, crew.morale_msg_good)
            else:
                $renpy.say(crew, crew.morale_msg_okay)
        "I want you on shields." if station_shields is not crew:
            call assign_station(crew, 'shields')
        "Help work the crops." if station_crops is not crew:
            call assign_station(crew, 'crops')
        "Monitor the engines." if station_engine is not crew:
            call assign_station(crew, 'engines')
        "Take a break.":
            if crew.morale < -3:
                call show_crew(crew, 'upset')
                "Oh, I was hoping you would say that."
            elif crew.morale > 3:
                call show_crew(crew, 'happy')
                "If you like, sir. But I'm ready to help whenever you need me!"
            else:
                "Thank you, sir. I'll try to relax a bit."
            call remove_from_stations(crew)
        "Nevermind":
            call hide_crew(crew)
            return

    PC "Thanks! That's all I needed."
    $renpy.say(crew, crew.bye)

    call hide_crew(crew)

    return
