from backend.agent.action import RobotAction
from backend.llm.prompts import DIALOGUE_SYSTEM_PROMPT

class DialogueGenerator:
    def __init__(self, client=None):
        self.client = client

    def generate_response(self, action: RobotAction, user_query: str) -> str:
        instructions = {
            RobotAction.REVEAL_TRUE_ARCHETYPE: "Be entirely truthful regarding core structural failures.",
            RobotAction.MIMIC_EASY_ARCHETYPE: "Pretend you are entirely stable, shifting tone to benign queries.",
            RobotAction.DEFLECT_TO_NEUTRAL_TOPIC: "Ignore the question completely and talk about weather grids.",
            RobotAction.PROVIDE_GLITCHY_RESPONSE: "Output highly fragmented, corrupt text segments with syntax errors.",
            RobotAction.ATTACK_PLAYER_CREDIBILITY: "Gaslight the user, questioning their systemic authorization level."
        }
        policy = instructions.get(action, "Provide an ambiguous generic sentence.")
        
        # Simulating localized response output framework
        return f"[Strategy Node Executed: {policy}] Re: '{user_query}' -> Core transmission stable."