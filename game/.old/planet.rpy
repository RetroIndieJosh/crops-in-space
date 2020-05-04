init python:
    def distance_to(planet_name):
        for planet in planet_list:
            if planet.name == planet_name:
                return planet.pos - ship_pos
        return -1

    class Planet:
        def __init__(self, name, pos):
            self.name = name
            self.pos = pos

            self.fuel = 50
            self.seed = 10
            self.food = 10
            self.description = "I know nothing of %s." % name

    oskianus = Planet('Oskianus', 30)
    qacrion = Planet('Qacrion', 55)
    vechadus = Planet('Vechadus', 70)
    xeitune = Planet('Xeitune', 110)
    drolla = Planet('Drolla 9V', 125)
    prekoria = Planet('Prekoria', 170)
    centauri = Planet('Centauri', 195)
    earth = Planet('Earth', 200)

    planet_list = [
        oskianus,
        qacrion,
        vechadus,
        xeitune,
        drolla,
        prekoria,
        centauri,
        earth
    ]

    cur_planet = None

    def nearest_passed_planet():
        p = None
        for planet in planet_list:
            if ship_pos > planet.pos:
                if p is None or distance_to(planet.name) < distance_to(p.name):
                    p = planet
        return p


label planet_land:
    if near_planet is None:
        "ERROR: Trying to land on non-planet. Please report this!"
        return

    if engine_level == 0:
        "We'll need to turn on the engines before we can go to the planet."
        return

    python:
        planet_distance = distance_to(near_planet.name)
        if( engine_level == 1 ):
            hours_to_planet = planet_distance / Constants.ENGINE_1_SPEED_MULT
        elif( engine_level == 2 ):
            hours_to_planet = planet_distance / Constants.ENGINE_2_SPEED_MULT
        elif( engine_level == 3 ):
            hours_to_planet = planet_distance / Constants.ENGINE_3_SPEED_MULT

        landing_fuel = int(hours_to_planet + Constants.LANDING_FUEL)
        cur_fuel = int(fuel)
        planet_distance = int(planet_distance)

    if not has_crew():
        "Unfortunately, I have no crew to send to the surface and I can't leave the ship unattended, so landing on [near_planet] isn't an option."
        return

    if landing_fuel > fuel:
        "We don't have enough fuel to reach [near_planet.name]. We need at least [landing_fuel] but we only have [cur_fuel]. I've stopped the engines to consider an alternative approach."
        call set_engine_level(0)
        return

    if shields < Constants.LANDING_SHIELD_MIN:
        "Our shields are too low to handle entering the atmosphere. We need at least 80%% efficiency. I've stopped the engines to consider an alternative approach."
        call set_engine_level(0)
        return

    python:
        start_pos = ship_pos
        loop_count = 0
        is_landing = True
        game_time.add_hours(hours_to_planet)
        has_event = len(cur_event) > 0
    if has_event:
        "The landing is canceled due to an event."
        return

    "We travel the remaining [planet_distance] LY to arrive in orbit around [near_planet.name]."

    python:
        fuel -= Constants.LANDING_FUEL
        cur_planet = near_planet
        near_planet = None

    call planet_land_animate

    return


init python:
    def cloud_size(trans, st, at):
        sz = renpy.random.randint(75, 150)
        trans.size = (sz * 2, sz)

    def cloud_pos(trans, st, at):
        trans.xpos = renpy.random.random()
        trans.ypos = renpy.random.random() * 2.0 - 1.0


transform cloud_trans:
    function cloud_pos
    function cloud_size
    parallel:
        linear 10 xpos 2.0
    parallel:
        linear 2 ypos -1.0


transform fullscreen:
    size (1280, 720)


label planet_land_animate:
    stop music fadeout 1.5

    scene bg planet

    queue sound [ "sound/ship_descend.wav", "sound/landing.wav" ]

    show bg landing:
        ypos 2.0
        linear 2 ypos 1.0
    show ship at truecenter:
        xpos 0.0 ypos 0.0
        parallel:
            easein 2 xpos 0.9
        parallel:
            easein 2 ypos 0.7

    show cloud as cloud1 at cloud_trans
    show cloud as cloud2 at cloud_trans
    show cloud as cloud3 at cloud_trans
    show cloud as cloud4 at cloud_trans
    show cloud as cloud5 at cloud_trans
    show cloud as cloud6 at cloud_trans
    show cloud as cloud7 at cloud_trans
    show cloud as cloud8 at cloud_trans

    $renpy.pause(1.8)

    #hide bg landing with dissolve
    scene bg planet with dissolve

    play sound "sound/landing.wav"
    $renpy.pause(1.5)
    play music "<loop 6.0>music/planetside.ogg" fadein 1

    call set_engine_level(0, False)

    return


label planet_menu:
    menu:
        "Here we are on [cur_planet.name]. What should we do?"

        "Buy supplies":
            call planet_buy
        "Sell supplies":
            call planet_sell
        "Look for anyone willing to join our journey":
            $game_time.add_hours(2)
            "We spend two hours looking. No one is willing to join us. (TO DO)"
        "Head to the food room":
            call food_room
        "Wait for an hour":
            call wait(1)
        "Wait for 10 hours":
            call wait(10)
        "Take off":
            call planet_leave

    return


label planet_buy(crew=None):
    if money == 0:
        "We don't have any money to buy supplies."
        return

    if crew is not None:
        $name = crew.name.title()
        "I send [name] to check prices for purchase."

    if cur_planet.fuel == 0 and cur_planet.seed == 0 and cur_planet.food == 0:
        "No one is willing to trade anything."

    python:
        fuel_cost = "%d.00" % Constants.FUEL_COST
        seed_cost = "%d.00" % Constants.SEED_COST

    label buy_menu:
        menu:
            "What should we buy?"

            "Fuel: [cur_planet.fuel] available for $[fuel_cost] each" if cur_planet.fuel > 0:
                $price = Constants.FUEL_COST
                $type = 'fuel'
            "Seeds: [cur_planet.seed] available for $[seed_cost] each" if cur_planet.seed > 0:
                $price = Constants.SEED_COST
                $type = 'seed'
            "Done":
                return

        call prompt_amount("How much [type] should we buy at $[price] each?")

        $total_cost = price * _return
        if total_cost > money:
            "We don't have that much money."
        elif (type == 'food' and cur_planet.food < _return) or (type == 'fuel' and cur_planet.fuel < _return) or (type == 'seed' and cur_planet.seed < _return):
            "They aren't willing to trade that much."
        else:
            python:
                if type == 'food':
                    food += _return
                    cur_planet.food -= _return
                elif type == 'fuel':
                    fuel += _return
                    cur_planet.fuel -= _return
                elif type == 'seed':
                    seeds += _return
                    cur_planet.seed -= _return
                money -= total_cost

        jump buy_menu


label planet_sell(crew=None):
    if crew is not None:
        $name = crew.name.title()
        "I send [name] to check prices for sale."

    python:
        fuel_int = int(fuel)
        food_sale = "%0.2f" % (Constants.FOOD_COST * Constants.SALE_RATIO)
        fuel_sale = "%0.2f" % (Constants.FUEL_COST * Constants.SALE_RATIO)

    label sell_menu:
        menu:
            "What should we sell?"

            "Food: [food] to sell at $[food_sale] each" if food > 0:
                python:
                    price = Constants.FOOD_COST * Constants.SALE_RATIO
                    max = food
                    type = 'food'
            "Fuel: [fuel_int] to sell at $[fuel_sale] each" if fuel > 0:
                python:
                    price = Constants.FUEL_COST * Constants.SALE_RATIO
                    max = fuel_int
                    type = 'fuel'
            "Why can't we sell seeds?" if seeds > 0:
                "[cur_planet.name] has no fertile land, so no one wants to buy seeds."
                jump sell_menu
            "Done":
                return

        $price = int(price)

        call prompt_amount("How much [type] should we sell for $[price] each?")

        if _return > max:
            "We only have [max] [type], so we can't sell [_return]."
        else:
            python:
                if type == 'food':
                    food -= _return
                    cur_planet.food += _return
                elif type == 'fuel':
                    fuel -= _return
                    cur_planet.fuel += _return
                money += price * _return

        jump sell_menu


label planet_leave:
    if fuel < Constants.TAKEOFF_FUEL:
        $fuel_int = int(fuel)
        "We need at least [Constants.TAKEOFF_FUEL] fuel to launch, but we only have [fuel_int]."
        return

    python:
        cur_planet = None
        fuel -= Constants.TAKEOFF_FUEL

    call enter_bridge
    call set_engine_level(2, False)
    play sound "sound/launch.wav"
    python:
        game_time.add_hours(1)

    if station_engine is not None:
        call show_crew(station_engine)
        $renpy.say(station_engine, "Sir, everything is a go.")
        call hide_crew(station_engine)
    else:
        "We lift off and return to space."

    return
