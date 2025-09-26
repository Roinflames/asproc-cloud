'''
Aprendizaje por refuerzos (RL)
Entrenamiento
Python y Machine Learning
'''
import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import deque

# Red neuronal simple para aproximar Q(s,a)
class DQN(nn.Module):
    def __init__(self, state_size, action_size):
        super(DQN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_size, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, action_size)
        )
    
    def forward(self, x):
        return self.net(x)

class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)  # memoria replay
        self.batch_size = 64
        self.gamma = 0.99  # factor de descuento
        self.epsilon = 1.0  # exploración inicial
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.policy_net = DQN(state_size, action_size).to(self.device)
        self.target_net = DQN(state_size, action_size).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()
        self.update_target_every = 10  # episodios para actualizar target net
        self.step_count = 0

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.action_size)  # acción aleatoria
        else:
            state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            with torch.no_grad():
                q_values = self.policy_net(state)
            return q_values.argmax().item()

    def store_transition(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def update(self):
        if len(self.memory) < self.batch_size:
            return

        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).unsqueeze(1).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        dones = torch.FloatTensor(dones).unsqueeze(1).to(self.device)

        current_q = self.policy_net(states).gather(1, actions)
        next_q = self.target_net(next_states).max(1)[0].detach().unsqueeze(1)
        expected_q = rewards + (self.gamma * next_q * (1 - dones))

        loss = self.loss_fn(current_q, expected_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Decay de epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_network(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())


def main():
    env = gym.make('CartPole-v1')
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n

    agent = Agent(state_size, action_size)

    episodes = 500

    for episode in range(episodes):
        state, info = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            agent.store_transition(state, action, reward, next_state, done)
            agent.update()

            state = next_state
            total_reward += reward

        # Actualizar target network cada 10 episodios
        if episode % agent.update_target_every == 0:
            agent.update_target_network()

        print(f"Episode: {episode+1}, Total Reward: {total_reward:.2f}, Epsilon: {agent.epsilon:.3f}")

if __name__ == "__main__":
    main()
    