
SHADOW_DIVIDER = 4

class Shape:
    coords: [[int]]
    color: (int, int, int)
    shadow_color: (int, int, int)

    def __init__(self, coords, color):
        self.color = color
        self.coords = coords

        self.__generate_shadow_color()

    # Takes the normal color and calculates the shadow-color
    def __generate_shadow_color(self):
        self.shadow_color = (
            self.color[0] / SHADOW_DIVIDER,
            self.color[1] / SHADOW_DIVIDER,
            self.color[2] / SHADOW_DIVIDER
        )
