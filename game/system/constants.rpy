init python in constants:
    EARTH_DISTANCE = 200

    FOOD_SALE = 15
    FUEL_SALE = 3
    SEED_SALE = 8

    FOOD_COST = 150
    FUEL_COST = 10
    SEED_COST = 30

    FOOD_PER_CROP = 2

    FUEL_LANDING = 2
    FUEL_TAKEOFF = 3
    FUEL_IDLE = 0.5
    FUEL_RUNNING = 0.5

    SHIELD_MIN_LANDING = 80
    SHIELD_CHARGE_PER_HOUR = 7

    SPEED_WARP = [0, 1, 3, 6]

    START_HOUR = int(renpy.random.random() * 24)

    START_FUEL = 30
    START_MONEY = 300
    START_FOOD = 5
    START_SHIELDS = 50
    START_SEEDS = 10

    START_CROP_SLOTS = 3

    MORALE_MAX = 10
    MORALE_LEAVE = -10

    # how much morale lost per hour (good = 1, okay = 0, bad = -1)
    MORALE_PER_HR_GOOD = 0.1
    MORALE_PER_HR_OKAY = 0.5
    MORALE_PER_HR_BAD = 1.0

    # extra growth per hour of crops when station occupied
    CROP_STATION_BONUS_MULT = 0.5
