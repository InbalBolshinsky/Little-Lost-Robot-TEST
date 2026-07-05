from typing import List

class RobotTemplate:
    def __init__(self, bot_id: str, archetype: str, descriptions: List[str]):
        self.bot_id = bot_id
        self.archetype = archetype
        self.descriptions = descriptions