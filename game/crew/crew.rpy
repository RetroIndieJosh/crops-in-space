init python in crew:
    list = []

    class Crew:
        def __init__(self, name, image_tag, gender="male", married=False):
            self.name = name
            name_split = self.name.split()
            self.name_first = name_split[0]
            if len(name_split) == 2:
                self.name_last = name_split[1]
            else:
                print("The name '%s' splits into %d words and only 1 or 2 names are supported." % (self.name, len(name_split)))
            self.image = image_tag

            self.gender = gender
            if self.gender == "male":
                self.pronoun_sub = "he"
                self.pronoun_obj = "him"
                self.possessive = "his"
                self.name_formal = "Mr. %s" % self.name_last
            elif self.gender == "other":
                self.pronoun_sub = "they"
                self.pronoun_obj = "them"
                self.possessive = "their"
                self.name_formal = "Mx. %s" % self.name_last
            else:
                self.honorific = "ma'am"
                self.pronoun_sub = "she"
                self.pronoun_obj = "her"
                self.possessive = "her"
                if married:
                    self.name_formal = "Mrs. %s" % self.name_last
                else:
                    self.name_formal = "Ms. %s" % self.name_last

            # skill levels
            self.engine_xp = 0
            self.engine_level = 0
            self.crops_xp = 0
            self.crops_level = 0
            self.shields_xp = 0
            self.shields_level = 0

            # ren'py "function" labels
            self.hello = image_tag + "_hello"
            self.bye = image_tag + "_bye"
            self.morale = image_tag + "_morale"
            self.affinity = image_tag + "_affinity"

            self.affinity_dict = {}

        def show(self, mood='neutral'):
            renpy.show("%s %s" % (self.image, mood))

        def hide(self):
            renpy.hide(self.image)


    def add(crew):
        for other_crew in list:
            crew.affinity_dict[other_crew.name] = 0
            other_crew.affinity_dict[crew.name] = 0
        list.append(crew)

    def remove(crew):
        for other_crew in list:
            del crew.affinity_dict[other_crew]
            del other_crew.affinity_dict[crew]
        list.remove(crew)

    def count():
        return len(list)

    def menu(prefix):
        choices = []
        choices.append(("Nevermind", 0))
        for i in range(len(list)):
            name = list[i].name
            pair = ("%s %s" % (prefix, name), i+1)
            choices.append(pair)
        result = renpy.display_menu(choices)

        if result == 0:
            return None
        return list[result-1]

    def menu_affinity(crew):
        choices = []
        choices.append(("Nevermind", 0))
        for i in range(len(list)):
            if list[i] == crew:
                continue
            name = list[i].name
            pair = ("How do you feel about %s?" % name, i+1)
            choices.append(pair)
        result = renpy.display_menu(choices)

        if result == 0:
            return None
        return list[result-1]


label crew_leave(crew):
    $crew.show('upset')
    $renpy.say(crew, "I can't stick around. A space taxi is here for me.")
    PC "Maybe I can change your mind?"
    $renpy.say(crew, "I'm sorry, but there are better opportunities for me out there.")
    call remove_from_stations(crew)
    $crew.on_ship = False
    $crew.hide()
    return


label crew_menu(prefix):
        # TODO move to the room where the crewmember is stationed
    $count = crew.count()
    if count == 0:
        "No crewmembers are on board."
        return
    $target = crew.menu(prefix)
    return target


label crew_talk_to(target):
    $has_hello = target.hello != None
    if not has_hello:
        "Looks like [target.name] has nothing to say."

    call crew_hello(target)
    call crew_menu_main(target)
    call crew_bye(target)
    $target.hide()
    return


label crew_hello(target):
    python:
        target.show()
        renpy.call(target.hello)
    return


label crew_bye(target):
    $renpy.call(target.bye)
    return


label crew_menu_main(target):
    $first_time = True
    while True:
        menu:
            target.character "[target.prompt]"

            "Ask about a crewmember":
                call crew_menu_affinity(target)
                $renpy.call(target.affinity, _return)
            "Nevermind" if first_time:
                return
            "That's all for now." if not first_time:
                return
        $first_time = False
    return


label crew_menu_affinity(target):
    $result = crew.menu_affinity(target)
    return result


label remove_from_stations(target):
    python:
        target.resting = True
        if station_shields is target:
            station_shields = None
        if station_crops is target:
            station_crops = None
        if station_engine is target:
            station_engine = None
    return
