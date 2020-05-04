init python:
    KLAARA = "Klaara Wekisa"
    K = Character('Klaara Wekisa')

    import store.crew as crew

    klaara = crew.Crew(KLAARA, "klaara", "female")

    klaara.character = K
    klaara.prompt = "Yes?"

    klaara.crops = 1
    klaara.engine = 0
    klaara.shields = -1

    crew.add(klaara)


label klaara_hello:
    return


label klaara_bye:
    show klaara happy
    K "Bye."

    return


label klaara_affinity(crew):
    python:
        if crew.name in klaara.affinity_dict:
            knows_crew = True
        else:
            knows_crew = False
    if not knows_crew:
        show klaara upset
        N "No idea."
        return

    $affinity = klaara.affinity_dict[crew.name]
    show klaara neutral
    N "Indeed, [crew.name_formal] is a member of our crew."
    return


label klaara_morale:
    if klaara.morale > 2:
        show klaara happy
        K "Most excellent."
    elif klaara.morale < 2:
        show klaara upset
        K "Not good."
    else:
        show klaara neutral
        K "Adequate."

    return
