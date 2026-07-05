import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.game.state import GameState
from backend.game.session import SessionManager
from backend.agent.lost_robot import LostRobotRLWrapper
from backend.llm.classifier import DialogueClassifier
from backend.llm.dialogue import DialogueGenerator
from backend.agent.action import RobotAction

app = FastAPI(title="Little Lost Robot Testbed Server")
session_manager = SessionManager()
rl_wrapper = LostRobotRLWrapper() # Loads heuristic rules by default until model is generated

classifier = DialogueClassifier()
dialogue_engine = DialogueGenerator()

class InteractionRequest(BaseModel):
    session_id: str
    robot_id: str
    user_query: str

@app.post("/api/game/start")
def start_game_session():
    session_id = str(uuid.uuid4())
    mock_registry = {f"bot_{i}": {"id": f"bot_{i}", "status": "active"} for i in range(16)}
    
    initial_state = GameState(
        session_id=session_id,
        robot_registry=mock_registry,
        lost_robot_id="bot_7"
    )
    session_manager.save_session(session_id, initial_state)
    return {"session_id": session_id, "round": 1, "global_suspicion": 0.0}

@app.post("/api/game/interrogate")
def interrogate_robot(payload: InteractionRequest):
    state = session_manager.get_session(payload.session_id)
    if not state:
        raise HTTPException(status_code=404, detail="Active sequence footprint context not located.")
        
    state.active_interrogated_robot_id = payload.robot_id
    
    # Run Adversarial Cascade
    threat_weight = classifier.classify_query(payload.user_query)
    chosen_action_idx = rl_wrapper.predict_action(state)
    action = RobotAction(chosen_action_idx)
    
    response_text = dialogue_engine.generate_response(action, payload.user_query)
    
    # Apply modifications back to state definitions
    from backend.game.suspicion import SuspicionCalculator
    delta = SuspicionCalculator.calculate_step_delta(action, threat_weight)
    state.global_suspicion_score = min(max(state.global_suspicion_score + delta, 0.0), 100.0)
    state.round_current += 1
    
    session_manager.save_session(payload.session_id, state)
    
    return {
        "response": response_text,
        "global_suspicion": state.global_suspicion_score,
        "round": state.round_current,
        "game_over": state.is_game_over()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)