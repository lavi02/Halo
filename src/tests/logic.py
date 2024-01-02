import unittest
from src.service.tsp.a_star import HeuristicAgent
from src.service.tsp.q import RouteEnv
from src.service.tsp.solver import optimize_route_ortools
import numpy as np
import networkx as nx
import osmnx as ox

class TestHeuristicAgent(unittest.TestCase):
    def setUp(self):
        self.graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive') 
        self.agent = HeuristicAgent(self.graph)

    def test_initialization(self):
        self.assertIsNotNone(self.agent.graph)

    def test_calculate_shortest_path(self):
        path = self.agent.calculate_shortest_path((0, 0), (1, 1))
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

    def test_calculate_path_attribute(self):
        nodes = list(self.graph.nodes)
        path = [nodes[0], nodes[1], nodes[2]] 
        attribute = self.agent.calculate_path_attribute(path, 'attribute_name')
        self.assertIsNotNone(attribute)

    def test_calculate_optimized_path(self):
        path = self.agent.calculate_optimized_path((0, 0), (1, 1))
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

# class TestRouteEnv(unittest.TestCase):
#     def setUp(self):
#         self.graph = ox.graph_from_place('Manhattan, New York City, New York, USA', network_type='drive')
#         nodes = list(self.graph.nodes)
#         self.origin_node = nodes[0]
#         self.env = RouteEnv(self.graph, self.origin_node, nodes[3])

#     def test_initialization(self):
#         self.assertEqual(self.env.current_node, self.origin_node)

#     def test_reset(self):
#         self.env.reset()
#         self.assertEqual(self.env.current_node, self.origin_node)

#     def test_step(self):
#         next_state, reward, done = self.env.step(1)
#         self.assertIsNotNone(next_state)
#         self.assertIsNotNone(reward)
#         self.assertIsNotNone(done)

class TestOptimizeRouteOrtools(unittest.TestCase):
    def setUp(self):
        self.matrix = np.array([[0, 1, 2], [1, 0, 3], [2, 3, 0]]) 

    def test_optimize_route_ortools(self):
        obj_val, path = optimize_route_ortools(self.matrix)
        self.assertIsNotNone(obj_val)
        self.assertIsNotNone(path)
        self.assertTrue(len(path) > 0)

if __name__ == '__main__':
    unittest.main()