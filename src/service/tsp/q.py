import osmnx as ox
import networkx as nx
import numpy as np
import random


class RouteEnv:
    def __init__(self, graph, origin_node, destination_node):
        self.graph = graph
        self.origin_node = origin_node
        self.destination_node = destination_node
        self.current_node = self.origin_node
        self.num_actions = len(list(graph.neighbors(self.current_node)))

    def reset(self):
        self.current_node = self.origin_node
        self.num_actions = len(list(self.graph.neighbors(self.current_node)))
        return self.current_node

    def step(self, action):
        neighbors = list(self.graph.neighbors(self.current_node))
        next_node = neighbors[action]

        reward = -self.graph[self.current_node][next_node][0]['length']
        self.current_node = next_node

        done = self.current_node == self.destination_node
        return self.current_node, reward, done


class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0):
        self.env = env
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.q_table = np.zeros(
            (len(self.env.graph.nodes), len(self.env.graph.edges)))

    def choose_action(self, state):
        '''
        Chooses an action based on the current state

        Args:
            state: The current state

        Returns:
            The action to be taken
        '''
        available_actions = len(list(self.env.graph.neighbors(state)))
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(range(available_actions))
        else:
            action = np.argmax(self.q_table[state, :available_actions])
        return action

    def update(self, state, action, reward, next_state):
        predict = self.q_table[state, action]
        target = reward + self.gamma * np.max(self.q_table[next_state, :])
        self.q_table[state, action] += self.lr * (target - predict)

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = self.env.reset()
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update(state, action, reward, next_state)
                state = next_state


# 도로 네트워크 로드 필요
def optimize_route(graph, origin_point, destination_point, num_episodes=1000):
    origin_node = ox.get_nearest_node(graph, origin_point)
    destination_node = ox.get_nearest_node(graph, destination_point)

    env = RouteEnv(graph, origin_node, destination_node)
    agent = QLearningAgent(env)

    agent.train(num_episodes)

    current_state = origin_node
    path = [current_state]

    while current_state != destination_node:
        action = np.argmax(agent.q_table[current_state, :])
        current_state = list(graph.neighbors(current_state))[action]
        path.append(current_state)

    return path
