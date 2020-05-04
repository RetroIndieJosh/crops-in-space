init python:
    ## add these values to each character

    # - extraversion, + introversion
    #e.world = 0

    # - sensing, + intuition
    #e.information = 0

    # - thinking, + feeling
    #e.decisions = 0

    # - judging, + perceiving
    #e.structure = 0

    positive_match_list = [ "ENFJ ENFJ", "ENFJ ENTJ", "ENFP ENFJ", "ENFP ENFP", "ENTJ ENTJ", "ENTP ENTP", "ENTP INTP", "ESFJ ENFP", "ESTJ ENTJ", "ESTJ ESFJ", "ESTJ INTJ", "ESTJ ISFJ", "ESTJ ISTP", "ESTP ESFP", "ESTP ESTP", "ESTP ISTJ", "INFJ ENFJ", "INFJ ENFP", "INFJ ENTP", "INFJ INFJ", "INFJ INFP", "INFP ENFJ", "INFP ENFP", "INFP INFP", "INTJ ENTJ", "INTJ INTJ", "INTJ ISTP", "INTP ENTP", "INTP INTJ", "INTP INTP", "ISFJ ENFJ", "ISFJ ISFJ", "ISFP ESFP", "ISFP ISFP", "ISTJ ESTJ", "ISTJ INTJ", "ISTJ ISTJ", "ISTP ENTJ", "ISTP ESTP", "ISTP ISTJ" ]

    negative_match_list = [ "INFP ESTJ", "INFP ISTJ", "INFP ESTP", "INFP ISTP", "INFP ENTJ", "INFP INTJ", "ENFP ISTJ", "ENFP ESTJ", "ENFP ISTP", "ENFP ESTP", "ENFP ISFJ", "ENFJ ESTJ", "ENFJ ESTP", "ENFJ ISTP", "ENFJ INTJ", "INTJ ESFJ", "INTJ ISFJ", "INTJ ESTP", "INTJ ESFP", "INTJ ISFP", "INTJ ENTP", "INTP ESFJ", "INTP ISFJ", "INTP ISTP", "INTP ESFP", "INTP ISFP", "ENTP ESFJ", "ENTP ISFJ", "ENTP ISTP", "ENTP ISFP", "ENTJ ESFJ", "ENTJ ISFJ", "ENTJ ESFP", "ENTJ ISFP ", "ISTJ ESFJ", "ISTJ ESFP", "ISTP ISTP", "ISTP ESFP", "ISTP INFJ", "ESTP ESFJ", "ESTP INFJ", "ESTJ INFJ", "ESFJ ESTP", "ESTP INFJ" ]

    def get_mb(c):
        if c.world > 0:
            world = 'I'
        else:
            world = 'E'

        if c.information > 0:
            information = 'N'
        else:
            information = 'S'

        if c.decisions > 0:
            decisions = 'F'
        else:
            decisions = 'T'

        if c.structure > 0:
            structure = 'P'
        else:
            structure = 'J'

        return world + information + decisions + structure

    def test_matches():
        narrator("ENFJ + ISTP = " + str(check_match('ENFJ', 'ISTP'))
            + "\nISTJ + ENTJ = " + str(check_match('ENFJ', 'ENTJ'))
            + "\nENFJ + ENTJ = " + str(check_match('ENFJ', 'ENTJ')))

    def check_match(mb1, mb2):
        combined1 = mb1 + ' ' + mb2
        combined2 = mb2 + ' ' + mb1
        for match in positive_match_list:
            if match == combined1 or match == combined2:
                return 1
        for match in negative_match_list:
            if match == combined1 or match == combined2:
                return -1
        return 0

    def show_mb(c):
        narrator("personality type: " + get_mb(c))
