import unittest
from unittest.mock import patch, MagicMock
from src.service.tsp.tsp import run
import networkx as nx

class TestRunFunction(unittest.TestCase):

    def setUp(self):
        self.mock_logger = MagicMock()
        self.mock_korea_network = nx.complete_graph(5)  # 테스트에 사용할 가짜 그래프
        self.matrix = [[0, 1, 2, 3, 4],
                       [1, 0, 1, 2, 3],
                       [2, 1, 0, 1, 2],
                       [3, 2, 1, 0, 1],
                       [4, 3, 2, 1, 0]]  # 테스트에 사용할 거리 행렬

    @patch('src.service.tsp.tsp.download_korea_road_network')
    @patch('src.service.tsp.tsp.create_distance_matrix')
    @patch('src.service.tsp.solver.OrToolsRouteOptimizer.optimize_route')
    @patch('src.service.tsp.solver.QLearningRouteOptimizer.optimize_route')
    @patch('src.service.tsp.solver.AStarRouteOptimizer.optimize_route')
    @patch('src.service.tsp.tsp.handler', new_callable=MagicMock)
    def test_run_success(self, mock_handler, mock_a_star_optimize, mock_q_learning_optimize, mock_ortools_optimize, mock_create_matrix, mock_download_network):
        mock_download_network.return_value = self.mock_korea_network
        mock_create_matrix.return_value = self.matrix
        mock_ortools_optimize.return_value = (100, [0, 1, 2, 3, 4])
        mock_q_learning_optimize.return_value = (150, [0, 1, 2, 3, 4])
        mock_a_star_optimize.return_value = (120, [0, 1, 2, 3, 4])

        waypoints = {"A": (0, 0), "B": (1, 1), "C": (2, 2), "D": (3, 3), "E": (4, 4)}
        result = run(waypoints)
        self.assertIsNotNone(result)
        self.assertIn("A", result)
        mock_handler.log.info.assert_called()

    def test_run_failure(self):
        with patch('src.service.tsp.tsp.download_korea_road_network', side_effect=Exception("Error")):
            with patch('src.service.tsp.tsp.handler.log.error') as mock_error:
                waypoints = {"A": (0, 0), "B": (1, 1), "C": (2, 2), "D": (3, 3), "E": (4, 4)}
                result = run(waypoints)
                self.assertEqual(result, {})
                mock_error.assert_called()



if __name__ == '__main__':
    unittest.main()
