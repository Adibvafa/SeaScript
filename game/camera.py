class Camera:
    pos: tuple[float, float]
    scale: float = 20.0

    def __init__(self, pos: tuple[float, float]):
        self.pos = pos
