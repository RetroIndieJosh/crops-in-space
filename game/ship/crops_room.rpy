label menu_crops():
    menu:
        "I'm in the crops room. What should I do?"

        #"Plant seeds" if seeds > 0 and crop_slots > 0:
            #call plant_seeds
            #jump food_room_loop
        #"Check crops" if crop_count > 0:
            #call crops_check
            #jump food_room_loop
        "Check crops":
            call screen crop_display()
        "Return to bridge":
            $game.set_location(game.loc_bridge)
    return


label plant_seeds():
    $available_slots = crop_max - count_crops()
    if available_slots < seeds:
        $new_seeds = available_slots
    else:
        $new_seeds = seeds

    python:
        seeds -= new_seeds
        for i in range(0, new_seeds):
            add_crop()
        crop_count = count_crops()
    "We plant [new_seeds] seeds. Now we have [crop_count] crops growing and [seeds] seeds left."

    return
