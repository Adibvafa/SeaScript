from game.entities.entity import Entity
from game.entities.player import Player
from game.qa import qa

class ObjectiveEntity(Entity):
    interacted_with: bool = False

    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        super().__init__(pos, size)

    def interact(self, player: Player):
        pass


def on_complete(player: Player):
    player.freeze_movement = False


class ChallengeEntity(ObjectiveEntity):

    def __init__(self, pos: tuple[float, float], size: tuple[float, float], challenge_num: int):
        super().__init__(pos, size)
        self.challenge_num = challenge_num

    def interact(self, player: Player):
        player.freeze_movement = True
        qa.open_challenge(self.challenge_num, lambda: on_complete(player))


class Objective:

    def __init__(self, description: str):
        self.description = description
        self.completed = False

    def check(self):
        pass

    def goal(self) -> tuple[float, float] | None:
        return None


class ObjectiveInteract(Objective):

    def __init__(self, description: str, entity: ObjectiveEntity):
        super().__init__(description)
        self.entity = entity

    def check(self):
        if self.entity.interacted_with:
            self.completed = True

    def goal(self) -> tuple[float, float] | None:
        return self.entity.pos


class ObjectiveCompleteChallenge(Objective):

    def __init__(self, challenge_num: int):
        super().__init__(f"Complete challenge {challenge_num}")
        self.challenge_num = challenge_num

    def check(self):
        if self.challenge_num in qa.completed_challenges:
            self.completed = True


objectives = []


def init_objectives():
    global objectives
    objectives = [
        ObjectiveInteract("Find the Queen Jellyfish", )
    ]