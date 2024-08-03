class Player:
    def __init__(self, pos: tuple[float, float]):
        self.pos = pos

    def __str__(self):
        return f'Player {self.name} is {self.age} years old'