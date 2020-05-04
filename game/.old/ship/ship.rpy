init python as ship:
    pos = 0

    def update(dhr):
        # TODO should check events on each update and only run up to elapsed hours if the update doesn't finish
        update_crops(hours)
        update_engine(hours)
        update_shields(hours)
        update_morale(hours)
        check_event()

init python:
    cur_enemy = None

    # ship movement (LY and LYPH)
    ship_pos = 0
    near_planet = None
    ship_speed = 1
    is_landing = False

    engine_level = 0
    shields_charging = False

    # stations
    station_crops = None
    station_engine = None
    station_shields = None

    # crops
    crop_list = []
    crop_max = Constants.START_CROP_MAX

    # supplies
    food = Constants.START_FOOD
    money = Constants.START_MONEY
    fuel = Constants.START_FUEL
    shields = Constants.START_SHIELDS
    seeds = Constants.START_SEEDS

    class Threshold:
        LOW_FUEL = 5
        LOW_FOOD = 4
        LOW_MORALE = -10
        PLANET = 10
        ENEMY = 5


    class ShipEvent:
        APPROACHING_PLANET = 2
        ARRIVED_EARTH = 3
        LOW_FUEL = 4
        LOW_FOOD = 5
        LOW_MORALE = 6
        NO_FUEL = 7
        NO_FOOD = 8
        PASSED_PLANET = 9
        LANDING_PLANET = 10
        NEW_DAY = 11
        ENEMY_ENCOUNTER = 12
        SHIELDS_CHARGED = 13


    cur_event = []
    fuel_alert = False


    def add_fuel(amount):
        global fuel
        fuel += amount
        fuel_alert = False


    def random_crew():
        on_ship_list = [x for x in crew_list if x.on_ship and x.name != 'player']
        return renpy.random.choice(on_ship_list)


    def update_engine(dhr):
        global earth_distance, engine_level, fuel, ship_pos

        # idle fuel consumption
        fuel_use = dhr * Constants.FUEL_IDLE_PER_HR
        if engine_level > 0:
            fuel_use += dhr * Constants.FUEL_RUNNING_PER_HR

        if fuel < fuel_use:
            fuel = 0
            if not fuel_alert:
                cur_event.append( ShipEvent.NO_FUEL )
                global fuel_alert
                fuel_alert = True
            return

        start_fuel = fuel
        fuel -= fuel_use

        if start_fuel > Threshold.LOW_FUEL and fuel < Threshold.LOW_FUEL:
            cur_event.append( ShipEvent.LOW_FUEL )

        # move ship
        move = 0
        if engine_level == 1:
            move = dhr * Constants.ENGINE_1_SPEED_MULT
        elif engine_level == 2:
            move = dhr * Constants.ENGINE_2_SPEED_MULT
        elif engine_level == 3:
            move = dhr * Constants.ENGINE_3_SPEED_MULT
        ship_pos += move

        # check enemy encounter
        if len(enemy_list) > 0:
            distance = enemy_list[0].pos - ship_pos
            if move > distance:
                move = distance
                cur_event.append(ShipEvent.ENEMY_ENCOUNTER)
                global cur_enemy, enemy_list
                cur_enemy = enemy_list[0]
                enemy_list.remove(cur_enemy)


    def update_morale(dhr):
        if station_crops is not None:
            if station_crops.crops > 0:
                station_crops.morale -= Constants.MORALE_PER_HR_GOOD * dhr
            elif station_crops.crops < 0:
                station_crops.morale -= Constants.MORALE_PER_HR_BAD * dhr
            else:
                station_crops.morale -= Constants.MORALE_PER_HR_OKAY * dhr
        if station_shields is not None:
            if station_shields.shields > 0:
                station_shields.morale -= Constants.MORALE_PER_HR_GOOD * dhr
            elif station_shields.shields < 0:
                station_shields.morale -= Constants.MORALE_PER_HR_BAD * dhr
            else:
                station_shields.morale -= Constants.MORALE_PER_HR_OKAY * dhr
        if station_engine is not None:
            if station_engine.shields > 0:
                station_engine.morale -= Constants.MORALE_PER_HR_GOOD * dhr
            elif station_engine.shields < 0:
                station_engine.morale -= Constants.MORALE_PER_HR_BAD * dhr
            else:
                station_engine.morale -= Constants.MORALE_PER_HR_OKAY * dhr
        for crew in crew_list:
            if crew.on_ship and crew.resting:
                crew.morale += dhr
            if crew.morale < Constants.MORALE_LEAVE:
                crew.morale = Constants.MORALE_LEAVE
            if crew.morale > Constants.MORALE_MAX:
                crew.morale = Constants.MORALE_MAX


    def list_resting():
        for crew in crew_list:
            if crew.on_ship and crew.resting:
                print(crew.name + ', ')


    def update_shields(dhr):
        global fuel, shields, shields_charging
        if not shields_charging:
            return
        charge_per_hour = Constants.SHIELD_CHARGE_PER_HOUR
        if station_shields is not None:
            charge_per_hour = int(charge_per_hour * 1.5)
        shields += dhr * charge_per_hour
        fuel -= dhr
        if shields >= 100:
            cur_event.append(ShipEvent.SHIELDS_CHARGED)
            shields = 100
            shields_charging = 0


label set_engine_level(lvl, show_msg=True):
    python:
        prev_engine_level = engine_level
        engine_level = lvl

    if engine_level > 0:
        python:
            if engine_level == 1:
                pace = 'normal pace.'
            elif engine_level == 2:
                pace = 'hurried pace.'
            elif engine_level == 3:
                pace = 'rapid pace. We\'ll get there in no time!'
        if prev_engine_level < engine_level:
            play sound "sound/engine_on.wav"
            play ambient "sound/engine_ambient.wav"
            show bg ship with hpunch
            if engine_level > 1:
                show bg ship with vpunch
            if engine_level > 2:
                show bg ship with pixellate

            if show_msg:
                "The engines spark to life and we start moving at a [pace]"
        else:
            if show_msg:
                "We slow down to a [pace]"
    else:
        stop ambient
        if prev_engine_level > 0:
            if show_msg:
                "The engines are off, and we stop moving."
        if shields_charging:
            $shields_charging = False
            if show_msg:
                "With the engines off, the shields are no longer charging."

    return


label enter_bridge:
    play music 'music/space.ogg' fadein 3
    scene bg ship with irisout
    return
