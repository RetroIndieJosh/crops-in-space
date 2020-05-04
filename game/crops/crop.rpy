init python:
    class Crop:
        SEED = 0
        SEEDLING = 1
        YOUNG = 2
        MATURE = 3

        def __init__(self, type):
            self.state = Crop.SEED
            self.type = type

        def get_image(self):
            return "crop %s %s" % (self.type, self.get_state_name())

        def get_state_name(self):
            if self.state == Crop.SEED:
                return "seed"
            elif self.state == Crop.SEEDLING:
                return "seedling"
            elif self.state == Crop.YOUNG:
                return "young"
            elif self.state == Crop.MATURE:
                return "mature"

        def grow(self):
            if self.state == Crop.SEED:
                self.state = Crop.SEEDLING
            elif self.state == Crop.SEEDLING:
                self.state = Crop.YOUNG
            elif self.state == Crop.YOUNG:
                self.state = Crop.MATURE
            elif self.state == Crop.MATURE:
                return False
            return True
