from src.service.tsp.q import nx, ox, np
from src.service.tsp.hvsine import create_graph, create_haversine_matrix
from src.service.tsp.solver import RouteOptimizer, OrToolsRouteOptimizer, QLearningRouteOptimizer, AStarRouteOptimizer
from typing import List

import pandas as pd
from src.repo.log.__init__ import handler

def download_korea_road_network() -> nx.Graph:
    try:
        korea_gdf = ox.geocode_to_gdf("Seoul, South Korea")
        korea_graph = ox.graph_from_polygon(
            korea_gdf.unary_union, network_type='drive', simplify=True)
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

    def run(self, matrix, start_fixed=False, end_fixed=False) -> tuple:
        best_value = float('inf')
        best_path = None

        for optimizer in self.optimizers:
            try:
                value, path = optimizer.optimize_route(matrix, start_fixed, end_fixed)
                if value < best_value:
                    best_value = value
                    best_path = path
            except Exception as e:
                handler.log.error("Error occurred while running optimizer: %s" % e)

        return best_value, best_path


def run(waypoints: dict, start_fixed: bool = False, end_fixed: bool = False) -> dict:
    try:
        korea = download_korea_road_network()
        coords = list(waypoints.values())

        # 출발지나 도착지를 고정하는 경우, 해당 지점을 리스트의 시작 또는 끝으로 이동
        if start_fixed or end_fixed:
            fixed_point = coords.pop(0) if start_fixed else coords.pop()
            matrix = create_distance_matrix(korea, coords)
            coords.insert(0, fixed_point) if start_fixed else coords.append(fixed_point)
        else:
            matrix = create_distance_matrix(korea, coords)

        optimizers = [OrToolsRouteOptimizer(logger=handler), QLearningRouteOptimizer(logger=handler), AStarRouteOptimizer(logger=handler)]
        runner = RouteOptimizerRunner(optimizers)
        objective_value, path = runner.run(matrix, start_fixed, end_fixed)
        handler.log.info("Objective value: %s, Path: %s" % (objective_value, path))

        if objective_value == 0 or path is None:
            coords = list(waypoints.values())
            matrix = create_haversine_matrix(coords)

            data = create_graph(waypoints, matrix)
            path = nx.shortest_path(data, 0, len(waypoints) - 1, weight='weight')
            handler.log.info("Objective value: %s, Path: %s" % (objective_value, path))

            optimized_waypoints = {}
            for i, index in enumerate(path):
                optimized_waypoints[list(waypoints.keys())[i]] = coords[index]

            return optimized_waypoints

        optimized_waypoints = {}
        for i, index in enumerate(path):
            optimized_waypoints[list(waypoints.keys())[i]] = coords[index]

        return optimized_waypoints

    except Exception as e:
        handler.log.error("TSP error occurred: %s" % e)
        return {}

