import osmnx as ox
import networkx as nx


class HeuristicAgent:
    '''
    Heuristic Agent - A* algorithm

    Attributes:
        graph: The graph to be used for the algorithm

    Methods:
        calculate_shortest_path: Calculates the shortest path between two points
        calculate_path_attribute: Calculates the attribute of a path
        calculate_optimized_path: Calculates the optimized path between two points
    '''

    def __init__(self, graph):
        self.graph = graph

    def calculate_shortest_path(self, origin_point: float, destination_point: float, weight='length') -> list:
        '''
        Calculates the shortest path between two points

        Args:
            origin_point: The origin point
            destination_point: The destination point
            weight: The weight of the graph

        Returns:
            The shortest path between the two points
        '''
        origin_node = ox.get_nearest_node(self.graph, origin_point)
        destination_node = ox.get_nearest_node(self.graph, destination_point)
        try:
            shortest_path = nx.astar_path(
                self.graph, origin_node, destination_node, weight=weight)
            return shortest_path
        except nx.NetworkXNoPath:
            print("No path found between the specified nodes.")
            return None

    def calculate_path_attribute(self, path: list, attribute: str) -> float:
        '''
        Calculates the attribute of a path

        Args:
            path: The path to be used
            attribute: The attribute to be calculated

        Returns:
            The attribute of the path
        '''
        return sum(self.graph[path[i]][path[i + 1]][0].get(attribute, 0) for i in range(len(path) - 1))

    def calculate_optimized_path(self, origin_point: float, destination_point: float):
        '''
        Calculates the optimized path between two points

        Args:
            origin_point: The origin point
            destination_point: The destination point

        Returns:
            The optimized path between the two points
        '''
        shortest_path = self.calculate_shortest_path(
            origin_point, destination_point)
        if shortest_path is None:
            return None
        shortest_path_length = self.calculate_path_attribute(
            shortest_path, 'length')

        optimized_path = shortest_path
        optimized_path_length = shortest_path_length

        for i in range(1, len(shortest_path) - 1):
            path1 = self.calculate_shortest_path(
                origin_point, shortest_path[i])

            path2 = self.calculate_shortest_path(
                shortest_path[i], destination_point)

            path_length = self.calculate_path_attribute(path1, 'length') + \
                self.calculate_path_attribute(path2, 'length')

            if path_length < optimized_path_length:
                optimized_path = path1 + path2[1:]
                optimized_path_length = path_length

        return optimized_path
