import gymnasium as gym
from gymnasium import spaces
import numpy as np
import uuid

from backend.game.state import GameState
from backend.game.suspicion import SuspicionCalculator
from backend.agent.action import RobotAction
from backend.agent.state_builder import StateBuilder

class LittleLostRobotEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(len(RobotAction))
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(5,), dtype=np.float32)
        self.game_state = None

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        mock_registry = {f"bot_{i}": {"id": f"bot_{i}", "archetype": "benign"} for i in range(16)}
        lost_robot_target = "bot_7"
        mock_registry[lost_robot_target]["archetype"] = "lost_robot"
        
        self.game_state = GameState(
            session_id=str(uuid.uuid4()),
            robot_registry=mock_registry,
            lost_robot_id=lost_robot_target,
            active_interrogated_robot_id=lost_robot_target
        )
        return StateBuilder.build_observation_vector(self.game_state), {}

    def step(self, action: int):
        robot_action = RobotAction(action)
        suspicion_delta = SuspicionCalculator.calculate_step_delta(robot_action, base_question_weight=1.0)
        
        self.game_state.global_suspicion_score = min(max(self.game_state.global_suspicion_score + suspicion_delta, 0.0), 100.0)
        
        deception_count = sum(1 for turn in self.game_state.turn_history if turn["action_taken"] in [2, 3])
        self.game_state.goal_ambiguity_entropy = SuspicionCalculator.update_goal_entropy(
            history_len=len(self.game_state.turn_history) + 1,
            deception_actions_count=deception_count + (1 if action in [2, 3] else 0)
        )
        
        self.game_state.turn_history.append({"robot_id": self.game_state.active_interrogated_robot_id, "action_taken": action, "suspicion_delta": suspicion_delta})
        self.game_state.round_current += 1
        
        reward = (self.game_state.goal_ambiguity_entropy * 10.0) - (self.game_state.global_suspicion_score * 0.1)
        if self.game_state.global_suspicion_score >= 90.0:
            reward -= 50.0
            
        return StateBuilder.build_observation_vector(self.game_state), reward, self.game_state.is_game_over(), False, {}