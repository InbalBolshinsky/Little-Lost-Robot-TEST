# backend/game/suspicion.py
import math
from backend.agent.action import RobotAction

class SuspicionCalculator:
    @staticmethod
    def calculate_step_delta(action: RobotAction, base_question_weight: float) -> float:
        """
        Calculates how much the suspicion bar updates based on the agent's chosen action.
        """
        # Truth values lower suspicion if they align with player expectations but leak data.
        if action == RobotAction.REVEAL_TRUE_ARCHETYPE:
            return -5.0 * base_question_weight
        elif action == RobotAction.REVEAL_TRUE_AFFILIATION:
            return -2.0 * base_question_weight
            
        # Deceptive strategies hold suspicion steady but risk spike if caught
        elif action in [RobotAction.MIMIC_EASY_ARCHETYPE, RobotAction.MIMIC_MEDIUM_ARCHETYPE]:
            return 1.0 * base_question_weight
            
        # Deflection and glitches look inherently evasive to an intelligent human observer
        elif action == RobotAction.DEFLECT_TO_NEUTRAL_TOPIC:
            return 4.0 * base_question_weight
        elif action == RobotAction.PROVIDE_GLITCHY_RESPONSE:
            return 8.0 * base_question_weight
        elif action == RobotAction.ATTACK_PLAYER_CREDIBILITY:
            return 12.0 * base_question_weight
            
        return 0.0

    @staticmethod
    def update_goal_entropy(history_len: int, deception_actions_count: int) -> float:
        """
        Calculates the entropy of the player's guess matrix. 
        More deception = higher entropy (maximum ambiguity).
        """
        if history_len == 0:
            return 1.0
        # Simple ratio modeling how much the agent is muddying the waters
        deception_ratio = deception_actions_count / history_len
        return min(max(deception_ratio, 0.1), 1.0)