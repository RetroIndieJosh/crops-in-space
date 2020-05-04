init python:
    class Enemy:
        def __init__(self, name, pos):
            self.pos = pos
            self.name = name
            self.encountered = False

    enemy_list = [
        Enemy('Gartok', 40),
        Enemy('Rogaressan', 80),
        Enemy('Odaroldu', 130),
        Enemy('Vargern', 150),
        Enemy('Krasodysmalyak', 180)
    ]


image shield red = im.MatrixColor( "images/shield.png", im.matrix.tint(1.0, 0.0, 0.0))
image shield yellow = im.MatrixColor( "images/shield.png", im.matrix.tint(1.0, 1.0, 0.0))
image shield green = im.MatrixColor( "images/shield.png", im.matrix.tint(0.0, 1.0, 0.0))
image shield blue = im.MatrixColor( "images/shield.png", im.matrix.tint(0.0, 0.0, 1.0))

image laser red = im.MatrixColor( "images/laser.png", im.matrix.tint(1.0, 0.0, 0.0))
image laser yellow = im.MatrixColor( "images/laser.png", im.matrix.tint(1.0, 1.0, 0.0))
image laser green = im.MatrixColor( "images/laser.png", im.matrix.tint(0.0, 1.0, 0.0))
image laser blue = im.MatrixColor( "images/laser.png", im.matrix.tint(0.0, 0.0, 1.0))

init python:
    ship_y = 0
    ship_amp = 0.2
    ship_freq = 2

    def rand_x(trans, st, at):
        trans.xpos = renpy.random.random()

    def rand_y(trans, st, at):
        trans.ypos = renpy.random.random()

    def laser_sound(trans, st, at):
        renpy.sound.play("sound/laser.wav")


transform laser_shot:
    xanchor 0.5 yanchor 0.5
    xpos 2
    function rand_y
    function laser_sound
    linear 1.0 xpos -1.0
    pause 3.0
    repeat


transform shipmoveinwiggle(ship_x):
    parallel:
        xanchor 0.5 yanchor 0.5 ypos 0.5 xpos -0.1
        easein ship_x * 10 xpos ship_x
    parallel:
        ease ship_freq ypos 0.5 + ship_amp
        ease ship_freq ypos 0.5 - ship_amp
        repeat


transform wiggle(start_y=0.5):
    yanchor 0.5
    ypos start_y
    block:
        ease ship_freq ypos 0.5 + ship_amp
        ease ship_freq ypos 0.5 - ship_amp
        repeat


label battle_start:
    if cur_enemy is None:
        "ERROR Started battle with no enemy. Please report this!"
        return

    hide screen info_display
    play sound "sound/enemy_warning.wav"
    play music "<loop 3.42>music/battle.ogg"

    $ship_x = 0.5
    call show_space(ship_x)

    $laser_color = renpy.random.randint(0, 4)

    if laser_color == 0:
        show laser red at laser_shot
    elif laser_color == 1:
        show laser yellow at laser_shot
    elif laser_color == 2:
        show laser green at laser_shot
    else:
        show laser blue at laser_shot

    # skip intro transition
    if persistent.skip_battle_intro:
        show ship at wiggle:
            xpos 0.5
        if shields > 90:
            show shield blue at wiggle:
                xcenter 0.5
        elif shields > 60:
            show shield green at wiggle:
                xcenter 0.5
        elif shields > 30:
            show shield yellow at wiggle:
                xcenter 0.5
        else:
            show shield red at wiggle:
                xcenter 0.5
        return
    else:
        if shields > 90:
            show shield blue at shipmoveinwiggle(ship_x)
        elif shields > 60:
            show shield green at shipmoveinwiggle(ship_x)
        elif shields > 30:
            show shield yellow at shipmoveinwiggle(ship_x)
        else:
            show shield red at shipmoveinwiggle(ship_x)

    show ship at shipmoveinwiggle(ship_x)

    PC "Evasive maneuvers!"


init python:
    battle_done = False


label battle_menu:
    python:
        battle_done = False
        distress_beacon = False
        tried_negotiation = False

    show screen info_display

    label battle_loop:
        python:
            if distress_beacon:
                distress = 'The distress beacon is active. '
            else:
                distress = ''
            if shields == 0:
                distress += 'Our shields are down! '

            if count_crew() > 0:
                crew = random_crew()
                prompt = "We're under attack by %s. %sYour orders, sir?" % (cur_enemy.name, distress)
            else:
                crew = PC
                prompt = "I'm under attack by %s. %sWhat do I do?" % (cur_enemy.name, distress)

        $renpy.say(crew, prompt)

        menu:
            # decide amount of fuel to use
            "Try to escape" if fuel > 0:
                call battle_evade
            "Activate distress beacon" if not distress_beacon:
                $distress_beacon = True
            "Deactivate distress beacon" if distress_beacon:
                $distress_beacon = False
            "Wait for help (1 hour)" if distress_beacon and shields > 0:
                call battle_wait
            "Negotiate for peaceful passage by offering supplies" if not tried_negotiation:
                $tried_negotiation = True
                call battle_negotiate
            "Surrender":
                call battle_surrender

        if not battle_done:
            jump battle_loop

    $cur_enemy = None
    if cur_planet is None:
        call enter_bridge
    else:
        call planet_land_animate
    return


label battle_end_nearest_planet:
    $p = nearest_passed_planet()
    if p is None:
        $ship_pos -= 30
        "We're quite a bit off-course."
    else:
        $cur_planet = p
        call set_engine_level(0)
        "Looks like we're back on [p.name] again."
    $battle_done = True
    return


label battle_end_escape:
    $battle_done = True
    return


label battle_evade:
    menu:
        "How much fuel should we expend to escape?"

        "1 (15%% chance)":
            $fuel -= 1
            $chance = 0.15
            "We keep on at our normal pace, with extra maneuvers."
        "3 (35%% chance)" if fuel >= 3:
            $fuel -= 3
            $chance = 0.35
            "We push the engines a bit."
        "9 (75%% chance)" if fuel >= 10:
            $fuel -= 10
            $chance = 0.75
            "We strain the engines on full burn."
        "18 (100%% chance)" if fuel >= 30:
            $fuel -= 30
            $chance = 1.0
            "We push the engines to the brink."

    $roll = renpy.random.random()
    if roll < chance:
        #"With intense maneuvers, we manage to escape. ([roll])"
        "With intense maneuvers, we manage to escape."
        call battle_end_escape
    else:
        #"They manage to catch up to us anyway. ([roll])"
        "They manage to catch up to us anyway."

    return


label battle_wait:
    python:
        sound_list = []
        hits = renpy.random.randint(1, 3)
        if hits == 1:
            s = ''
        else:
            s = 's'
        for i in range(0, hits):
            sound_list.append("sound/shield_impact.wav")
        renpy.sound.queue(sound_list)
    "We take [hits] hit[s] while waiting for help."

    python:
        game_time.add_hours(1)

        prev_shields = shields
        shields -= 7 * hits
        shield_changed = False

    if shields > 60 and prev_shields >= 90:
        $print('shield green')
        $shield_changed = True
        show shield green at wiggle:
            xcenter 0.5
    elif shields > 30 and prev_shields >= 60:
        $shield_changed = True
        $print('shield yellow')
        show shield yellow at wiggle:
            xcenter 0.5
    elif shields < 30 and prev_shields >= 30:
        $shield_changed = True
        $print('shield red')
        show shield red at wiggle:
            xcenter 0.5
    elif shields < 1:
        $shield_changed = True
        $shields = 0
        "The shields are gone!"
        hide shield

    if shield_changed:
        show ship at wiggle with vpunch

    return


label battle_negotiate:
    "I hail the enemy ship, but they refuse to respond."
    return


label battle_surrender:
    "We surrender to the enemy. They strip us of all our fuel and food, and drop us at the nearest planet. Luckily, we have a hidden cache of money they didn't find."
    python:
        money = Constants.START_MONEY
        fuel = 0
        food = 0

        for crew in crew_list:
            if crew.on_ship:
                crew.morale -= 5
    call battle_end_nearest_planet
    return
