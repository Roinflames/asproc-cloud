'''
Aprendizaje por refuerzos (RL)
Entrenamiento
Python y Machine Learning
'''
import gymnasium as gym

class Agent:
    def __init__(self, env):
        self.action_space = env.action_space

    def select_action(self, state):
        return self.action_space.sample()

    def update(self, state, action, reward, next_state, done):
        pass

env = gym.make('CartPole-v1')
agent = Agent(env)

for episode in range(100):
    state, info = env.reset()  # gymnasium devuelve tupla (state, info)
    total_reward = 0
    done = False

    while not done:
        action = agent.select_action(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward

    print("Episode:", episode + 1, "Total Reward:", total_reward)
