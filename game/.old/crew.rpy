init python:
    class Crew(object):
        def __init__(self, real_char, on_ship=False, morale=0):
            self.name = real_char
            self.real_char = real_char
            self.on_ship = on_ship
            self.morale = morale
            self.rations = 1
            self.shields = 0
            self.engine = 0
            self.crops = 0
            self.greeting = "Yessir?"
            self.bye = "Thanks."
            self.resting = False
            self.morale_msg_bad = "I'm upset."
            self.morale_msg_good = "I'm happy."
            self.morale_msg_okay = "I'm okay."

        def __call__(self, what, interact=True):
            return getattr(store, self.real_char)(what, interact=interact)

        def predict(self, what):
            return getattr(store, self.real_char).predict(what)


    ning = Character('Ning Lang')
    N = Crew('ning', True, 5)
    N.engine = 1
    N.crops = -1
    N.greeting = "What can I do for you, sir?"
    N.bye = "Let me know if you need anything else."
    N.morale_msg_bad = "Can't you tell? Things aren't great. I hope they improve soon, or I don't what I'll do."
    N.morale_msg_good = "Things are great! Thank you for having me along. We'll be home any time now."
    N.morale_msg_okay = "Nothing to complain about, really. Let's keep pushing forward!"

    klaara = Character('Klaara Wekisa')
    K = Crew('klaara', True, 2)
    K.crops = 1
    K.shields = -1
    K.greeting = "Yes?"
    K.bye = "Indeed."
    K.morale_msg_bad = "Not good."
    K.morale_msg_good = "Most excellent."
    K.morale_msg_okay = "Adequate."

    edward = Character('Edward Lucan')
    E = Crew('edward')

    teobaldo = Character('Teobaldo Davidson')
    T = Crew('teobaldo')

    PC = Crew('player', True, 0)

    crew_list = [ N, K, E, T ]


label crew_leave(crew):
    call show_crew(crew, 'upset')
    $renpy.say(crew, "I can't stick around. A space taxi is here for me.")
    PC "Maybe I can change your mind?"
    $renpy.say(crew, "I'm sorry, but there are better opportunities for me out there.")
    call remove_from_stations(crew)
    $crew.on_ship = False
    call hide_crew(crew)
    return
