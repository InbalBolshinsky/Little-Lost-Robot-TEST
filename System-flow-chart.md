    FRONTEND:
                    React UI
                       │
                    REST API
                       │
                    BACKEND:
                    FastAPI
                    │     	│
          AGENT     	LLM
            layer     	layer
               │              		│
        state_builder    classifier.py
        lost_robot.py    dialogue.py
               │              		│
           PPO model      LLM API
           (frozen)
               │
           action enum
               │
          prompts.py
               │
          LLM API
               │
           dialogue
               │
            FRONTEND


**Example Data Flow:**

1. Player types question
   		│ HTTP POST /interrogate
   		▼
2. backend/llm/classifier.py
   → question_type (number)
   		│
   		▼
3. backend/agent/state_builder.py
   → state vector [0.45, 2, 0.1, 1, 6, 3]
   		│
   		▼
4. backend/agent/lost_robot.py
   → action (DEFLECT)
   		│
   		▼
5. backend/llm/prompts.py
   → builds prompt with action + archetype + question
   		│
   		▼
6. backend/llm/dialogue.py
   → calls Anthropic API
   → returns robot response
   		│
   		▼
7. backend/game/suspicion.py
   → updates suspicion score
   		│
   		▼
8. backend/game/state.py
   → updates game state
   		│ HTTP response
   		▼
9. Frontend displays dialogue
   Player updates suspicion board
