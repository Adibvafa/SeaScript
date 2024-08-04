from game.entities.entity import Entity
from game.entities.player import Player
from game.qa import qa
from game.world import world


class ObjectiveEntity(Entity):
    interacted_with: bool = False

    def __init__(self, pos: tuple[float, float], size: tuple[float, float]):
        super().__init__(pos, size)

    def interact(self, player: Player):
        pass


class ChallengeEntity(ObjectiveEntity):

    def __init__(self, pos: tuple[float, float], size: tuple[float, float], challenge_num: int):
        super().__init__(pos, size)
        self.challenge_num = challenge_num

    def on_complete(self, player: Player):
            self.interacted_with = True

    def interact(self, player: Player):
        if self.interacted_with:
            return
        qa.open_challenge(self.challenge_num, lambda: self.on_complete(player))


class Objective:

    def __init__(self, description: str):
        self.description = description
        self.completed = False

    def check(self):
        pass

    def goal(self) -> tuple[float, float] | None:
        return None


class ObjectiveInteract(Objective):

    entity: ObjectiveEntity

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
    from game.entities.QueenJelly import QueenJelly
    queen_jelly = QueenJelly((25.0, 50.0))
    from game.entities.KingShark import KingShark
    king_sharky = KingShark((150.0, 100.0))
    from game.entities.blank import BlankChallengeEntity
    blank = BlankChallengeEntity((180.0, 160.0))
    from game.entities.chest import Chest
    chest = Chest((239.0, 182.0))
    world.add_entity(queen_jelly)
    world.add_entity(king_sharky)
    world.add_entity(blank)
    world.add_entity(chest)
    objectives.append(ObjectiveInteract("Find the Queen Jellyfish", queen_jelly))
    objectives.append(ObjectiveCompleteChallenge(0))
    objectives.append(ObjectiveInteract("Find the King Shark", king_sharky))
    objectives.append(ObjectiveCompleteChallenge(1))
    objectives.append(ObjectiveInteract("Find the Coral Reef", blank))
    objectives.append(ObjectiveCompleteChallenge(2))
    objectives.append(ObjectiveInteract("Find the Treasure Chest", chest))
    objectives.append(ObjectiveCompleteChallenge(3))



def check_objectives():
    for objective in objectives:
        was_completed = objective.completed
        objective.check()
        if objective.completed and not was_completed:
            print(f"Completed objective: {objective.description}")


def get_current_objective() -> Objective | None:
    for objective in objectives:
        if not objective.completed:
            return objective
    return None


def get_closest_objective_entity(player: Player) -> ObjectiveEntity | None:
    entities = [e for e in world.entities if isinstance(e, ObjectiveEntity)]
    if len(entities) == 0:
        return None
    entities.sort(key=lambda e: (e.pos[0] - player.pos[0]) ** 2 + (e.pos[1] - player.pos[1]) ** 2)
    nearest = entities[0]
    curr_obj = get_current_objective()
    if isinstance(curr_obj, ObjectiveInteract) and curr_obj.entity == nearest:
        return nearest

    return None
