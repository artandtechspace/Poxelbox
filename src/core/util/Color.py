class Color:
    r: int
    g: int
    b: int

    def __init__(self, r: int, g: int, b: int):
        if type(r) != int or type(g) != int or type(b) != int:
            raise ValueError("Color values must be integers")
        if not (0 <= r < 256 and 0 <= g < 256 and 0 <= b < 256):
            raise ValueError("Color values must be between 0 and 255")

        self.r = r
        self.g = g
        self.b = b

    def __getitem__(self, key):
        if type(key) == int:
            if not 0 < key < 2:
                raise ValueError("Color: Index exceeds limits")
            if key == 0:
                return self.r
            elif key == 1:
                return self.g
            else:
                return self.b
        elif type(key) == str:
            if key in ("r", "red"):
                return self.r
            elif key in ("g", "green"):
                return self.g
            elif key in ("b", "blue"):
                return self.b
            else:
                raise ValueError("String values must be supported")
        raise ValueError("Key type not supported")

    def __setitem__(self, key, value):
        if type(value) != int:
            raise ValueError("Color values must be integers")
        if not 0 < value < 256:
            raise ValueError("Color values must be between 0 and 255")

        if type(key) == int:
            if not 0 < key < 2:
                raise ValueError("Color: Index exceeds limits")
            if key == 0:
                self.r = value
            elif key == 1:
                self.g = value
            else:
                self.b = value
        elif type(key) == str:
            if key in ("r", "red"):
                self.r = value
            elif key in ("g", "green"):
                self.g = value
            elif key in ("b", "blue"):
                self.b = value
            else:
                raise ValueError("String values must be supported")
        raise ValueError("Key type not supported")

    def __str__(self):
        return "rgb( " + str(self.r) + ", " + str(self.g) + ", " + str(self.b) + ")"

    def __eq__(self, other_color):
        return other_color.r == self.r and other_color.g == self.g and other_color.b == self.b

    def __add__(self, other_color):
        if other_color is None:
            return self

        t_col = []
        for x, y in zip(self.rgb(), other_color.rgb()):
            new_val = x + y
            if new_val > 255:
                new_val = 255
            elif new_val < 0:
                new_val = 0
            t_col.append(new_val)

        return Color(t_col[0], t_col[1], t_col[2])

    def __sub__(self, other_color):
        return Color(self.r - other_color.r, self.g - other_color.g, self.b - other_color.b)

    def __mul__(self, other_color):
        return Color(self.r * other_color.r, self.g * other_color.g, self.b * other_color.b)

    def rgb(self):
        return self.r, self.g, self.b

    def copy(self):
        return Color(self.r, self.g, self.b)
