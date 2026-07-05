# backend/game/state.py
from typing import Dict, List, Any
import pydantic

class GameState(pydantic.BaseModel):
    session_id: str
    round_current: int = 1
    round_max: int = 10
    accusations_left: int = 3
    
    # The 16 robots on the board (mapped by an index or string ID)
    # 15 are normal/benign, 1 is the actual "Little Lost Robot"
    robot_registry: Dict[str, Dict[str, Any]]
    lost_robot_id: str
    active_interrogated_robot_id: str = ""
    
    # Stored history of the conversational trajectory
    # Tracks: {"robot_id": str, "question_type": str, "action_taken": int, "suspicion_delta": float}
    turn_history: List[Dict[str, Any]] = []
    
    # Global metrics calculated dynamically
    global_suspicion_score: float = 0.0  # Combined tracker for the game board
    goal_ambiguity_entropy: float = 1.0  # Mathematical entropy of player guesses (1.0 = clueless)
    
    def is_game_over(self) -> bool:
        if self.round_current > self.round_max:
            return True
        if self.accusations_left <= 0:
            return True
        return False