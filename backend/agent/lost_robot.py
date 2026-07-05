import os
import numpy as np
from stable_baselines3 import PPO
from backend.agent.state_builder import StateBuilder
from backend.game.state import GameState

class LostRobotRLWrapper:
    def __init__(self, checkpoint_path: str = None):
        if checkpoint_path and os.path.exists(checkpoint_path):
            self.model = PPO.load(checkpoint_path)
        else:
            self.model = None # Fallback to heuristic rules if models aren't trained yet

    def predict_action(self, game_state: GameState) -> int:
        if self.model:
            obs = StateBuilder.build_observation_vector(game_state)
            action, _ = self.model.predict(obs, deterministic=True)
            return int(action)
        # Heuristic Rule Engine fallback
        if game_state.global_suspicion_score > 70.0:
            return 4 # Deflect
        return 2 # Mimic benign