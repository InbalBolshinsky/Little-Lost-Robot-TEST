import os
from stable_baselines3 import PPO
from rl.environment.env import LittleLostRobotEnv

def run_training_pipeline():
    os.makedirs("checkpoints/easy", exist_ok=True)
    env = LittleLostRobotEnv()
    
    print("Beginning Adversarial Policy Search Optimization via PPO...")
    model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.0003, n_steps=512, batch_size=64)
    model.learn(total_timesteps=5000)
    
    model.save("checkpoints/easy/model")
    print("Optimization parameter block saved successfully.")

if __name__ == "__main__":
    run_training_pipeline()