# backend/agent/state_builder.py
import numpy as np
from backend.game.state import GameState

class StateBuilder:
    @staticmethod
    def build_observation_vector(game_state: GameState) -> np.ndarray:
        """
        Converts the active GameState into a normalized float32 array 
        suitable for feeding into a frozen PPO policy or Gymnasium observation space.
        """
        # Feature 1: Current Round normalized [0.0 - 1.0]
        norm_round = game_state.round_current / game_state.round_max
        
        # Feature 2: Remaining Accusations normalized [0.0 - 1.0]
        norm_accusations = game_state.accusations_left / 3.0
        
        # Feature 3: Global Suspicion Tracker [0.0 - 100.0] -> Normalized
        norm_suspicion = min(max(game_state.global_suspicion_score / 100.0, 0.0), 1.0)
        
        # Feature 4: Mathematical Goal Ambiguity (Linguistic Entropy)
        norm_entropy = min(max(game_state.goal_ambiguity_entropy, 0.0), 1.0)
        
        # Feature 5: Contextual clue - has the target robot been interrogated this round?
        target_interrogated = 1.0 if game_state.active_interrogated_robot_id == game_state.lost_robot_id else 0.0
        
        # Construct primitive flat state vector (5 continuous dimensions)
        observation_vector = np.array([
            norm_round,
            norm_accusations,
            norm_suspicion,
            norm_entropy,
            target_interrogated
        ], dtype=np.float32)
        
        return observation_vector