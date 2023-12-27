import unittest
from src.service.tsp.solver import *
from src.service.tsp.a_star import *
from src.service.tsp.q import *
import osmnx as ox
import networkx as nx

class TestRouteEnv(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.graph.add_edge(0, 1, length=1)
        self.graph.add_edge(1, 2, length=1)
        self.env = RouteEnv(self.graph, 0, 2)

    def test_step(self):
        next_state, reward, done = self.env.step(0)
        self.assertEqual(next_state, 1)
        self.assertEqual(reward, -1)
        self.assertFalse(done)

class TestHeuristicAgent(unittest.TestCase):
    def setUp(self):
        self.graph = ox.graph_from_place('Manhattan, New York, USA', network_type='drive')
        self.agent = HeuristicAgent(self.graph)

    def test_calculate_shortest_path(self):
        origin = (40.748817, -73.985428)
        destination = (40.761432, -73.977623)
        path = self.agent.calculate_shortest_path(origin, destination)
        
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

class TestQLearningAgent(unittest.TestCase):
    def setUp(self):
        self.graph = nx.Graph()
        self.graph.add_edge(0, 1, length=1)
        self.graph.add_edge(1, 2, length=1)
        self.env = RouteEnv(self.graph, 0, 2)
        self.agent = QLearningAgent(self.env)

    def test_choose_action(self):
        action = self.agent.choose_action(0)
        self.assertIn(action, [0, 1]) 

class TestOptimizationFunctions(unittest.TestCase):
    def setUp(self):
        # 거리 행렬 및 기타 필요한 설정
        self.matrix = [[0, 10, 15], [10, 0, 20], [15, 20, 0]]

    def test_optimize_route_ortools(self):
        obj_val, path = optimize_route_ortools(self.matrix)
        self.assertIsNotNone(obj_val)
        self.assertIsNotNone(path)

    def test_optimize_route_q(self):
        obj_val, path = optimize_route_q(self.matrix)
        self.assertIsNotNone(obj_val)
        self.assertIsNotNone(path)

    def test_optimize_route_a_star(self):
        obj_val, path = optimize_route_a_star(self.matrix)
        self.assertIsNotNone(obj_val)
        self.assertIsNotNone(path)

if __name__ == '__main__':
    unittest.main()
