from rl.environment.env import LittleLostRobotEnv
from stable_baselines3 import PPO

def run_evaluation():
    env = LittleLostRobotEnv()
    model = PPO.load("checkpoints/easy/model")
    
    obs, _ = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, _, _ = env.step(action)
        total_reward += reward
    print(f"Evaluation Sequence Concluded. Cumulative Strategic Reward: {total_reward:.4f}")

if __name__ == "__main__":
    run_evaluation()