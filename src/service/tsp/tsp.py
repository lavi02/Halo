from src.service.tsp.q import *
from src.service.tsp.solver import *
from src.service.tsp.a_star import *

import pandas as pd
from src.repo.log.__init__ import handler

def download_korea_road_network() -> nx.Graph:
    try:
        korea_gdf = ox.geocode_to_gdf("South Korea")
        korea_graph = ox.graph_from_polygon(
            korea_gdf.unary_union, network_type='drive')
        return korea_graph
    except Exception as e:
        handler.log.error("Error downloading Korea road network: %s" % e)
        korea_graph = ox.graph_from_place('South Korea', network_type='drive')
        return korea_graph


def create_distance_matrix(graph, coords):
    df = pd.DataFrame(coords, columns=['y', 'x'])
    df['node'] = [ox.nearest_nodes(graph, x, y) for x, y in coords[::-1]]
    matrix = np.zeros((len(coords), len(coords)))

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            try:
                length = nx.shortest_path_length(
                    graph, df.at[i, 'node'], df.at[j, 'node'], weight='length')

                # 대칭성
                matrix[i][j] = length
                matrix[j][i] = length
            except nx.NetworkXNoPath:
                matrix[i][j] = float('inf')
                matrix[j][i] = float('inf')

    return matrix


class RouteOptimizerRunner:
    def __init__(self, optimizers: List[RouteOptimizer]):
        self.optimizers = optimizers

    def run(self, matrix) -> tuple:
        best_value = float('inf')
        best_path = None

        for optimizer in self.optimizers:
            value, path = optimizer.optimize_route(matrix)
            if value < best_value:
                best_value = value
                best_path = path

        return best_value, best_path


def run(waypoints: dict) -> dict:
    try:
        korea = download_korea_road_network()
        coords = list(waypoints.values())
        matrix = create_distance_matrix(korea, coords)

        optimizers = [OrToolsRouteOptimizer(logger=handler), QLearningRouteOptimizer(
            logger=handler), AStarRouteOptimizer(logger=handler)]
        runner = RouteOptimizerRunner(optimizers)
        objective_value, path = runner.run(matrix)
        handler.log.info("Objective value: %s, Path: %s" %
                         (objective_value, path))

        optimized_waypoints = {}
        for i, index in enumerate(path):
            optimized_waypoints[list(waypoints.keys())[i]] = coords[index]

        return optimized_waypoints

    except Exception as e:
        handler.log.error("TSP error occurred: %s" % e)
        return {}