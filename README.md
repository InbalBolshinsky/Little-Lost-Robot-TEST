# Little-Lost-Robot-TEST

Test repository for the "Little Lost Robot" game project.

## Project Structure

### Top Level

```text
little-lost-robot-test/
│
├── frontend/          # React UI
├── backend/           # FastAPI server
├── rl/                # Training code
├── checkpoints/       # Saved agent models
├── docs/              # GDD, research notes
└── README.md


frontend/
│
├── src/
│   ├── components/
│   │   ├── RobotGrid.jsx         # 4x4 grid of 16 robots
│   │   ├── RobotCard.jsx         # Individual robot portrait
│   │   ├── InterrogationPanel.jsx # Dialogue interface
│   │   ├── SuspicionBoard.jsx    # Player's notebook
│   │   └── GameStatus.jsx        # Rounds, accusations left
│   │
│   ├── hooks/
│   │   ├── useGameState.js       # Central game state
│   │   └── useInterrogation.js   # Handles question flow
│   │
│   ├── api/
│   │   └── gameClient.js         # Calls to FastAPI backend
│   │
│   └── App.jsx
│
└── package.json

backend/
│
├── main.py                  # FastAPI entry point
│
├── game/
│   ├── state.py             # GameState class
│   ├── robots.py            # Robot, NormalRobot classes
│   ├── archetypes.py        # 5 archetype rule tables
│   ├── suspicion.py         # Suspicion score calculator
│   └── session.py           # Manages active game sessions
│
├── agent/
│   ├── lost_robot.py        # RL agent wrapper
│   ├── state_builder.py     # Builds state vector from game state
│   └── action.py            # Action enum + descriptions
│
├── llm/
│   ├── classifier.py        # Classifies player question → type
│   ├── dialogue.py          # Generates robot responses
│   └── prompts.py           # All prompt templates
│
└── requirements.txt

rl/
│
├── environment/
│   ├── env.py               # Custom gymnasium.Env class
│   ├── simulated_player.py  # Heuristic player for training
│   └── reward.py            # Reward function
│
├── training/
│   ├── train.py             # PPO training loop
│   ├── evaluate.py          # Test agent performance
│   └── compare.py           # RL vs LLM only comparison
│
├── notebooks/
│   └── training.ipynb       # Google Colab notebook
│
└── configs/
    └── ppo_config.yaml      # Hyperparameters

checkpoints/
│
├── easy/
│   └── model.zip            # Episode 1,000
├── medium/
│   └── model.zip            # Episode 5,000
├── hard/
│   └── model.zip            # Episode 10,000
└── expert/
    └── model.zip            # Episode 20,000
