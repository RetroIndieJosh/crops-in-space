init python:
    NING = 'Ning Lang'
    N = Character(NING)

    import store.crew as crew

    ning = crew.Crew(NING, "ning", "female")

    ning.character = N
    ning.prompt = "What can I do for you, sir?"

    ning.crops = -1
    ning.engine = 1
    ning.shields = 0

    crew.add(ning)


label ning_hello:
    show ning happy
    N "Hello there!"

    return


label ning_bye:
    show ning happy
    N "Let me know if you need anything else!"

    return


label ning_affinity(target):
    python:
        if target.name in ning.affinity_dict:
            knows_crew = True
        else:
            knows_crew = False
    if not knows_crew:
        show ning upset
        N "I don't know anything about that person."
        return

    $affinity = ning.affinity_dict[target.name]
    show ning neutral
    N "Oh, [target.name_first]? [target.pronoun_sub] seems all right."
    return


label ning_morale:
    if ning.morale > 2:
        show ning happy
        N "Things are great! Thank you for having me along. We'll be home any time now."
    elif ning.morale < 2:
        show ning upset
        N "Can't you tell? Things aren't great. I hope they improve soon, or I don't what I'll do."
    else:
        show ning neutral
        N "Nothing to complain about, really. Let's keep pushing forward!"

    return
