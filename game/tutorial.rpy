label intro_scene:
    python:
        station_crops = K
        station_engine = N

    if persistent.skip_intro:
        call name_player
        scene bg ship
        play music 'music/space.ogg'
        return

    call show_space(0.5)

    show text "{size=40}GAME BY Joshua McLean{/size}" at creditleft with Dissolve(3)
    show text "{size=40}ART BY Kate Goebel{/size}" at creditright with Dissolve(3)
    show text "{size=60}C R O P S   I N   S P A C E{/size}" at top with Dissolve(3)
    hide text with Dissolve(1)

    "The incident left the three of us lost in the galaxy, but now Ning has found the way home."

    "Won't be an easy journey. We've made many enemies, and our ship's unique crop-growing technology makes a prime target. But we'll get home. Eventually."

    "We made a quick trade on this planet for seeds and fuel. No one was willing to trade food, but we still have a bit stored from what we've grown."

    "Food is a rare commodity out here. Lucky for us, this ship's systems were built for growing crops."

    call name_player

    "The course is set and the crew are ready."

    stop music fadeout 2.0

    call enter_bridge

    show ning neutral with dissolve
    N "Sir, the engines are fully operational. What speed would you like to move ahead?"

    call menu_engine

    if engine_level > 0:
        N "Good choice, sir."
    else:
        show ning upset
        N "Oh, we're not moving yet? As you wish. Simply head to the power room and change the engine level when you're ready."

    show ning neutral at left with ease

    show klaara neutral with dissolve
    $crop_count = count_crops()
    K "I've taken to working on the crops, sir. We have [crop_count] growing and a food supply of [food]."

    K "Would you like me to plant more seeds? We only have room for a limited number of crops at a time. Currently, we can plant [crop_max] seeds at a time."

    $max = crop_max - crop_count

    menu:
        "Yes":
            K "Good. We can plant up to [max] more."
            call prompt_amount( "Number of seeds to plant ([max] max):")
            $seeds_to_plant = _return
        "No":
            $seeds_to_plant = 0

    if seeds_to_plant == 0:
        show klaara upset
        K "Oh, you don't want to plant any? Okay."
    elif seeds_to_plant > max:
        show klaara upset
        K "Sir, we can't plant that many. Oh, are you joking? Okay, let me know when you're ready to be more serious."

    python:
        seeds -= seeds_to_plant
        for i in (0, seeds_to_plant):
            add_crop()

    show klaara neutral
    K "You can always head to the food room to plant more seeds. We can also convert food to fuel or harvest seeds from food."

    K "Seeds will grow into food after ten hours, but {b}only{/b} if the engines are on."

    show klaara neutral at right with ease
    N "That's sort of right. The engine needs fuel to be at least idling for the crop systems to run. We need less fuel to idle than we do while moving."

    N "Level 2 is faster than Level 1, but crops will only grow at 50%% efficiency."

    K "And they won't grow at all when we're at Level 3. All the power goes to the engines, then."

    N "We also need someone at the engine controls to make sure it doesn't overheat at Level 3, so you won't be able to put the engine at Level 3 unless someone is there."

    K "Preferably not me. Plants are more my thing."

    "Before we start the journey, I should learn what I can from these two."

    call show_tutorial
    return

label show_tutorial:
    show klaara neutral at right
    show ning neutral at left
    $tutorial_done = False
    label tutorial_loop:
        menu:
            "How do I get more fuel?":
                K "Planets sell fuel."

                N "They have other supplies, too. We can buy seeds to grow into food, and turn the food into fuel on the ship."

            "How do I keep crew morale up?":
                show ning upset
                N "We'll get upset if we don't have anything to eat, or if you work us too hard."

                show ning happy
                N "You can always talk to us to give us a break!"

                show ning neutral
                show klaara upset
                K "Don't put us on a station we don't like."

                show klaara neutral
                N "Klaara's a biologist, so she's good with the crops. I'm more familiar with the engines."

            "How do I turn crops into food?":
                K "The ship will automatically harvest crops. Seeds will grow on their own. Go to the food room to plant seeds."

            "Tell me about landing on planets.":
                K "The ship will inform us when a planet is near."

                N "It's up to you if you want to land on planets, but it's a good idea. We can trade, do some work, and so on."

                K "Landing takes extra fuel. Launching even more."

                N "Yes, so watch that fuel meter! The ship will also alert you when that's low."

            "What happens if we encounter enemies?":
                show ning upset
                N "Yes, we've made a lot of enemies. A lot of people want our crop-growing tech, and some of them just want to finish the job..."

                K "This ship is not equipped with weapons."

                show ning neutral
                N "We've got shields, though! We can always try to run away, or negotiate with them. Even if they hate us, they might be reasonable."

                K "One can hope."

                N "Head to the power room to charge shields. This takes extra fuel, and the engines need to be at least Level 1."

            "Thank you, officers. Please return to your stations.":
                $tutorial_done = True

        if not tutorial_done:
            jump tutorial_loop

    ning "Yessir!" (multiple=2)
    klaara "Indeed." (multiple=2)

    hide ning with dissolve
    hide klaara with dissolve

    return
