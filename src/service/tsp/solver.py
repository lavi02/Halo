from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from multiprocessing import Pool
import pandas as pd
import osmnx as ox
import networkx as nx

from src.repo.log.__init__ import handler
from src.service.tsp.a_star import *
from src.service.tsp.q import *


def create_data_model(matrix):
    data = {}
    data['distance_matrix'] = matrix

    data['num_vehicles'] = 1
    data['depot'] = 0

    return data


def optimize_route_ortools(matrix):
    """
    Args:
        matrix: The distance matrix

    Returns:
        The objective value and the solution
    """
    try:
        # Instantiate the data problem
        data = create_data_model(matrix)
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']), data['num_vehicles'], data['depot'])

        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int(data['distance_matrix'][from_node][to_node])

        transit_callback_index = routing.RegisterTransitCallback(
            distance_callback)

        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        solution = routing.SolveWithParameters(search_parameters)

        if solution:
            handler.log.info("Objective: %s" % solution.ObjectiveValue())
            handler.log.info("Route: ")

            objective_value = solution.ObjectiveValue()
            path = []
            index = routing.Start(0)

            while not routing.IsEnd(index):
                path.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))

            path.append(manager.IndexToNode(index))

            return objective_value, path
        else:
            return None, None

    except Exception as e:
        handler.log.error("Ortools error: %s" % e)
        return None, None


def optimize_route_q(matrix):
    """
    Args:
        matrix: The distance matrix

    Returns:
        The objective value and the solution
    """
    try:
        graph = nx.from_numpy_array(np.array(matrix))
        origin_node = 0
        destination_node = len(matrix) - 1

        env = RouteEnv(graph, origin_node, destination_node)
        agent = QLearningAgent(env)
        agent.train(1000)

        state = env.reset()
        done = False
        path = [state]

        while not done:
            action = agent.choose_action(state)
            next_state, _, done = env.step(action)
            path.append(next_state)
            state = next_state

        objective_value = 0
        for i in range(len(path) - 1):
            objective_value += matrix[path[i]][path[i + 1]]

        return objective_value, path

    except Exception as e:
        handler.log.error("Q error: %s" % e)
        return None, None


def optimize_route_a_star(matrix):
    """
    Args:
        matrix: The distance matrix

    Returns:
        The objective value and the solution
    """
    try:
        graph = nx.from_numpy_array(np.array(matrix))
        origin_node = 0
        destination_node = len(matrix) - 1

        origin = graph.nodes[origin_node]['x'], graph.nodes[origin_node]['y']
        destination = graph.nodes[destination_node]['x'], graph.nodes[destination_node]['y']

        agent = HeuristicAgent(graph)
        path = agent.calculate_optimized_path(origin, destination)
        if path is None:
            return None, None

        objective_value = 0
        for i in range(len(path) - 1):
            objective_value += matrix[path[i]][path[i + 1]]

        return objective_value, path

    except Exception as e:
        handler.log.error("A* error: %s" % e)
        return None, None


def download_korea_road_network() -> nx.Graph:
    korea_gdf = ox.geocode_to_gdf("South Korea")
    korea_graph = ox.graph_from_polygon(
        korea_gdf.unary_union, network_type='drive')
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


def run(waypoints: dict) -> dict:
    """
    Args:
        waypoints: The waypoints
        - key: The waypoint name: str
        - value: The waypoint coordinate: tuple

    Returns:
        The optimized route
        - key: The waypoint name: str
        - value: The waypoint coordinate: tuple
    """
    try:
        korea = download_korea_road_network()
        coords = list(waypoints.values())
        matrix = create_distance_matrix(korea, coords)

        pool = Pool(processes=3)
        procs = []
        results = []

        procs.append(pool.apply_async(optimize_route_ortools, (matrix,)))
        procs.append(pool.apply_async(optimize_route_q, (matrix,)))
        procs.append(pool.apply_async(optimize_route_a_star, (matrix,)))

        for proc in procs:
            results.append(proc.get())

        pool.close()
        pool.join()

        objective_values = [result[0] for result in results]
        paths = [result[1] for result in results]

        min_index = objective_values.index(min(objective_values))
        path = paths[min_index]

        optimized_waypoints = {}
        for i, index in enumerate(path):
            optimized_waypoints[list(waypoints.keys())[i]] = coords[index]

        return optimized_waypoints

    except Exception as e:
        handler.log.error("TSP error occurred: %s" % e)
        return {}
