import json
import random
from collections import defaultdict, deque

def load_graph(filepath="railway_graph.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def build_adjacency_list(data):
    adj = defaultdict(list)
    for edge in data["edges"]:
        src = edge["source"]
        dest = edge["destination"]
        weight = edge["distance"]
        adj[src].append((dest, weight))
    return adj

def bellman_ford(graph, source):
    distance = {node: float('inf') for node in graph}
    predecessor = {node: None for node in graph}
    distance[source] = 0

    for _ in range(len(graph) - 1):
        for u in graph:
            for v, w in graph[u]:
                if distance[u] + w < distance[v]:
                    distance[v] = distance[u] + w
                    predecessor[v] = u

    # Optional: Detect negative-weight cycles
    for u in graph:
        for v, w in graph[u]:
            if distance[u] + w < distance[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    return distance, predecessor

# ---------- FORD-FULKERSON (Max Flow) ----------
def bfs(residual_graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)

    while queue:
        u = queue.popleft()
        for v, capacity in residual_graph[u].items():
            if v not in visited and capacity > 0:
                queue.append(v)
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
    return False

def ford_fulkerson(graph, source, sink):
    residual_graph = defaultdict(dict)

    # Initialize residual graph
    for u in graph:
        for v, capacity in graph[u]:
            residual_graph[u][v] = capacity
            if v not in residual_graph or u not in residual_graph[v]:
                residual_graph[v][u] = 0  # reverse edge with 0 capacity

    parent = {}
    max_flow = 0

    while bfs(residual_graph, source, sink, parent):
        # Find minimum residual capacity along the path filled by BFS
        path_flow = float('inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_graph[parent[s]][s])
            s = parent[s]

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            residual_graph[u][v] -= path_flow
            residual_graph[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow

    return max_flow

# utils/graph_utils.py
import random

def simulate_congestion_points(graph_data):
    points = []
    for edge in graph_data["edges"]:
        lat = edge.get("source_lat")
        lng = edge.get("source_lng")
        if lat and lng:
            points.append({
                "lat": lat,
                "lng": lng,
                "weight": random.randint(1, 10)  # simulate traffic weight
            })
    return points
