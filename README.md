
# Little-Lost-Robot-TEST

test repo for "Little Lost Robot" game project

Project structure:

* Top level:

**little-lost-robot-test/**
│
├── frontend/          # React UI
├── backend/           # FastAPI server
├── rl/                # Training code
├── checkpoints/       # Saved agent models
├── docs/              # GDD, research notes
└── README.md

**frontend/**
│
├── src/
│   ├── components/
│   │   ├── RobotGrid.jsx        # 4x4 grid of 16 robots
│   │   ├── RobotCard.jsx        # individual robot portrait
│   │   ├── InterrogationPanel.jsx  # dialogue interface
│   │   ├── SuspicionBoard.jsx   # player's notebook
│   │   └── GameStatus.jsx       # rounds, accusations left
│   │
│   ├── hooks/
│   │   ├── useGameState.js      # central game state
│   │   └── useInterrogation.js  # handles question flow
│   │
│   ├── api/
│   │   └── gameClient.js        # calls to FastAPI backend
│   │
│   └── App.jsx
│
└── package.json

**backend/**
│
├── main.py                  # FastAPI entry point
│
├── game/
│   ├── state.py             # GameState class
│   ├── robots.py            # Robot, NormalRobot classes
│   ├── archetypes.py        # 5 archetype rule tables
│   ├── suspicion.py         # suspicion score calculator
│   └── session.py           # manages active game sessions
│
├── agent/
│   ├── lost_robot.py        # RL agent wrapper
│   ├── state_builder.py     # builds state vector from game state
│   └── action.py            # action enum + descriptions
│
├── llm/
│   ├── classifier.py        # classifies player question → type
│   ├── dialogue.py          # generates robot responses
│   └── prompts.py           # all prompt templates
│
└── requirements.txt

**rl/**
│
├── environment/
│   ├── env.py               # custom gymnasium.Env class
│   ├── simulated_player.py  # heuristic player for training
│   └── reward.py            # reward function
│
├── training/
│   ├── train.py             # PPO training loop
│   ├── evaluate.py          # test agent performance
│   └── compare.py           # RL vs LLM only comparison
│
├── notebooks/
│   └── training.ipynb       # Google Colab notebook
│
└── configs/
    └── ppo_config.yaml      # hyperparameters

**checkpoints/**
│
├── easy/
│   └── model.zip            # episode 1,000
├── medium/
│   └── model.zip            # episode 5,000
├── hard/
│   └── model.zip            # episode 10,000
└── expert/
    └── model.zip            # episode 20,000
