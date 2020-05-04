init python:
    import store.game as game

    def get_info():
        t = "Day %d, %02d:00" % (game.day, game.hour)

        pos = "Earth: %d light years" % (200 - game.pos)

        supplies = "$%d\nFood: %d\nFuel: %d\nSeeds: %d" % (game.money, game.food, game.fuel, game.seeds)

        basic_info = "%s\n%s\n%s" % (t, pos, supplies)

        ship_info = "Shields: %d\nWarp: %d" % (game.shields, game.warp)

        return "%s\n%s" % (basic_info, ship_info)

screen info_display():
    default show_info = True

    showif show_info:
        frame:
            xpadding 20
            text "\n%s\n" % (get_info()) id 'info' style 'monospace'
        textbutton "Hide Info" action SetScreenVariable("show_info", False)
    showif not show_info:
        frame:
            textbutton "Show Info" action SetScreenVariable("show_info", True)
