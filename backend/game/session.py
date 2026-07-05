from typing import Dict
from backend.game.state import GameState

class SessionManager:
    def __init__(self):
        self.active_sessions: Dict[str, GameState] = {}
        
    def get_session(self, session_id: str) -> GameState:
        return self.active_sessions.get(session_id)
        
    def save_session(self, session_id: str, state: GameState):
        self.active_sessions[session_id] = state