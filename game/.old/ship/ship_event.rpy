init python:
    # TODO this should be event_list
    cur_event = []

    def check_event():
        #TODO check for events here
        # low fuel
        # low food
        # low morale (crewmember wants off)
        # approaching planet
        # entering conflict
        # arrived at earth

        if distance_to('Earth') <= 0:
            cur_event.append( ShipEvent.ARRIVED_EARTH )

        check_near_planet()


    def check_near_planet():
        if cur_planet is not None:
            return

        # clear "near" planet when we're past it
        global near_planet, ship_pos, cur_event, planet_list
        if near_planet is not None:
            if ship_pos >= near_planet.pos and not is_landing:
                near_planet = None
                cur_event.append( ShipEvent.PASSED_PLANET )
            return

        # find next near planet (if we aren't near one)
        for planet in planet_list:
            if planet.pos < ship_pos:
                continue
            distance = planet.pos - ship_pos
            if distance > 0 and distance < Threshold.PLANET:
                near_planet = planet
                cur_event.append( ShipEvent.APPROACHING_PLANET )
                return


    def distance_to(planet_name):
        for planet in planet_list:
            if planet.name == planet_name:
                return planet.pos - ship_pos
        return -1
