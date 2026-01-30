class BBox:
    def __init__(
        self, x_min: int, y_min: int, x_max: int, y_max: int, text: str, name: str
    ) -> None:
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.text = text
        self.name = name

    def __str__(self) -> str:
        return f"{self.name=}[[{self.x_min}, {self.y_min}], [{self.x_max}, {self.y_max}]] \n {self.text=}"
