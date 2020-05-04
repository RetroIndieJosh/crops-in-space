init python:
    # growth_rate in % per hour
    class Crop():
        def __init__(self):
            self.name = "Turnip"
            self.growth = 0
            self.mature_hours = Constants.CROP_GROW_HR
            self.elapsed_hours = 0
            self.food_amount = Constants.FOOD_PER_CROP

        def grow(self, dhr):
            if engine_level == 3:
                return

            if engine_level == 2:
                dhr *= 0.5

            self.elapsed_hours += dhr
            self.growth = (self.elapsed_hours / self.mature_hours) * 100
            print("Grow %f => %f" % (dhr, self.growth) )

        def is_food(self):
            return self.growth >= 100

        def __repr__(self):
            return self.__str__()

        def __str__(self):
            return "%s (%d hr, %0.2f%%)" % (self.name, self.mature_hours, self.growth)


    def add_crop():
        global crop_max
        if count_crops() + 1 > crop_max:
            return None
        c = Crop()
        crop_list.append(c)
        return c


    def count_crops():
        return len(crop_list)


    def update_crops(dhr):
        global crop_list, food, fuel

        # can't grow crops without fuel
        if fuel <= 0:
            return

        for crop in crop_list:
            crop.grow(dhr)
            if station_crops is not None:
                crop.grow(dhr * Constants.CROP_STATION_BONUS_MULT)
            if(crop.is_food()):
                food += crop.food_amount
        crop_list = [x for x in crop_list if not x.is_food()]


label crops_check:
    python:
        crop_count = count_crops()
        crop_status = ''
        for crop in crop_list:
            crop_status += '%s: %d%%, ' % (crop.name, crop.growth)
        crop_status = crop_status[:-2]
        if engine_level == 3 or fuel == 0:
            e = 0
        elif engine_level == 2:
            e = 50
        else:
            e = 100
        efficiency = "Crops are growing at %d%% efficiency." % e


    "[efficiency] We have the following [crop_count] crops: [crop_status]."

    return
