import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
import imageio



video_file = "lunar_lander_render.mp4"
fps = 30


env = gym.make("LunarLander-v3", render_mode="rgb_array")
env = DummyVecEnv([lambda: env])

model = DQN.load("dqn_lunar_lander.zip")

obs = env.reset()

writer = imageio.get_writer(video_file, fps=fps)
for _ in range(1000):
	action, _ = model.predict(obs, deterministic=True)
	obs, rewards, done, info = env.step(action)

	
	frame = env.render()
	writer.append_data(frame)


	if done:
		obs = env.reset()

writer.close()
env.close()		