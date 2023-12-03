import unittest
from src.service.tsp.solver import *
from src.service.tsp.a_star import *
from src.service.tsp.q import *


class TestOptimizeRoute(unittest.TestCase):
    def test_optimize_route(self):
        distance_matrix = [
            [0, 2, 9, 10],
            [1, 0, 6, 4],
            [15, 7, 0, 8],
            [6, 3, 12, 0],
        ]

        objective_value, solution = optimize_route(distance_matrix)

        self.assertIsNotNone(solution)
        self.assertIsInstance(objective_value, int)
        self.assertEqual(objective_value, 21)


if __name__ == '__main__':
    unittest.main()
