import math
import networkx as nx
import numpy as np

def haversine(coord1, coord2):
    # 지구 반지름 (km 단위)
    R = 6371.0

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def create_haversine_matrix(coords):
    num_coords = len(coords)
    matrix = np.zeros((num_coords, num_coords))
    for i in range(num_coords):
        for j in range(num_coords):
            if i != j:
                matrix[i][j] = haversine(coords[i], coords[j])
    return matrix


def create_graph(nodes, edges):
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    
    for edge in edges:
        node1, node2 = edge
        distance = haversine(nodes[node1], nodes[node2])
        G.add_edge(node1, node2, weight=distance)
    
    return G