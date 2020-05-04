init python:
    import store.crew as crew
    import store.game as game

label menu_bridge:
    #$crop_count = count_crops()
    show screen bridge_display
    menu:
        "I'm on the bridge. What should I do?"

        "Speak with a crewmember":
            call crew_menu("Speak with")
            if _return == None:
                return
            call crew_talk_to(_return)
        "Go to crops room":
            $game.set_location(game.loc_crops)
        "Go to power room":
            $game.set_location(game.loc_power)
        #"Land on [near_planet.name] to trade" if near_planet is not None:
            #call planet_land
        #"Head to the power room (shields and engine)":
            #$game.location = "power"
        #"Head to the crops room (crops and food)":
            #$game.location = "crops"
        #"Wait for an hour":
            #call wait(1)
        #"Wait for 10 hours":
            #call wait(10)
        #"Ask crew for help":
            #hide screen info_display
            #call show_tutorial
            #show screen info_display

        "Debug Menu" if persistent.debug_options:
            call menu_debug

    hide screen bridge_display
    return
