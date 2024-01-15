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
        # Use get method with a default value for missing 'length' attribute
        reward = -self.graph[self.current_node][next_node].get('length', 1)  # Default length can be 1 or any other value
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
        neighbors = list(self.env.graph.neighbors(state))
        num_available_actions = len(neighbors)
        if num_available_actions == 0:
            return -1
        
        available_actions = len(list(self.env.graph.neighbors(state)))
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(range(available_actions))
        else:
            action = np.argmax(self.q_table[state, :available_actions])
        return action

    def update(self, state, action, reward, next_state):
        '''
        Updates the Q-table

        Args:
            state: The current state
            action: The action to be taken
            reward: The reward for the action
            next_state: The next state
        '''
        if action == -1:  # 더 이상 이동할 수 없는 경우
            return
        
        available_actions = len(list(self.env.graph.neighbors(state)))
        if next_state == self.env.destination_node:
            self.q_table[state, action] = reward
        else:
            self.q_table[state, action] = self.q_table[state, action] + self.lr * (
                reward + self.gamma * float(np.max(self.q_table[next_state, :available_actions])) - self.q_table[state, action])

    def train(self, num_episodes):
        for episode in range(num_episodes):
            state = self.env.reset()
            done = False

            while not done:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update(state, action, reward, next_state)
                state = next_state

            self.epsilon = 1 - (episode / num_episodes)


# 도로 네트워크 로드 필요
def optimize_route(graph, origin_point, destination_point, num_episodes=1000):
    originX = origin_point[0]
    originY = origin_point[1]
    destinationX = destination_point[0]
    destinationY = destination_point[1]

    origin_node = ox.nearest_nodes(graph, originX, originY)
    destination_node = ox.nearest_nodes(graph, destinationX, destinationY)

    env = RouteEnv(graph, origin_node, destination_node)
    agent = QLearningAgent(env)
    agent.train(num_episodes)

    state = env.reset()
    done = False
    path = [state]

    while not done:
        action = agent.choose_action(state)
        next_state, _, done = env.step(action)
        state = next_state
        path.append(state)

    return path
