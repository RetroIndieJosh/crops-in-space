label menu_power:
    menu:
        "I'm in the power room. What should I do?"

        "Modify the engine level":
            call menu_engine
        #"Charge the shields" if shields < 100 and not shields_charging:
            #call charge_shields_start
        #"Stop charging the shields" if shields_charging:
            #call charge_shields_stop
        "Return to bridge":
            $game.set_location(game.loc_bridge)
    return


label menu_engine:
    if game.fuel == 0:
        "There's no fuel to run the engines."
        return

    menu:
        "What level should I put the engine on?"

        "Off" if game.warp != 0:
            call set_warp(0)
        "Warp 1 (Normal)" if game.warp != 1:
            call set_warp(1)
        "Warp 2 (Crop Growth 50%%)" if game.warp != 2:
            call set_warp(2)
        "Warp 3 (Crop Growth 0%%)" if game.warp != 3:
            call set_warp(3)
        "Leave it off" if game.warp == 0:
            return
        "Leave it on Warp [game.warp]" if game.warp > 0:
            return

    return


label charge_shields_start:
    if engine_level == 0:
        "The engines must be on before I can charge the shields."
        return

    $shields_charging = True
    play sound "sound/shield_charge.wav"
    "The shields are now charging."

    return


label charge_shields_stop:
    $shields_charging = False
    "The shields are no longer charging."
    return


label set_warp(warp):
    if warp == game.warp:
        return

    $game.warp = warp
    if game.warp > 0:
        play sound "sound/engine_on.wav"
        play ambient "sound/engine_ambient.wav"

    show bg power with hpunch
    if game.warp > 0:
        if game.warp > 1:
            show bg power with vpunch
        if game.warp > 2:
            show bg power with pixellate

        "The engines are now running at warp [game.warp]."
    else:
        "The engines are now off."
        stop ambient
    return
