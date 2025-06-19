from flask import Flask, render_template, request, jsonify
from utils.graph_utils import (
    load_graph,
    build_adjacency_list,
    bellman_ford,
    ford_fulkerson,
    simulate_congestion_points
)
import api_requests
import heapq

app = Flask(__name__)

@app.route("/")
def home():
    graph_data = load_graph()
    congestion_points = simulate_congestion_points(graph_data)

    # Define station coordinates FIRST
    station_coords = {
            "NDLS": (28.6139, 77.2090),
    "BCT": (18.9696, 72.8195),
    "HWH": (22.5806, 88.3495),
    "MAS": (13.0827, 80.2707),
    "SBC": (12.9784, 77.5695),
    "PNBE": (25.5941, 85.1376),
    "LKO": (26.8467, 80.9462),
    "GKP": (26.7606, 83.3732),
    "ADI": (23.0258, 72.5873),
    "CNB": (26.4499, 80.3319),
    "JBP": (23.1815, 79.9864),
    "BPL": (23.2599, 77.4126),
    "KYN": (19.1717, 72.9460),
    "CSTM": (18.9401, 72.8355),
    "GHY": (26.1445, 91.7362),
    "ASR": (31.6339, 74.8723),
    "JU": (26.2389, 73.0243),
    "BSB": (25.3176, 82.9739),
    "RJPB": (25.6093, 85.1235),
    "BJU": (25.4753, 86.0030),
    "TATA": (22.7841, 86.2029),
    "GAYA": (24.7969, 85.0002),
    "DBG": (26.1675, 85.8970),
    "KOAA": (22.5726, 88.3639),
    "DNR": (25.5941, 85.1376),
    "UMB": (30.3681, 76.7880),
    "ET": (22.6526, 78.7594),
    "KGP": (22.3402, 87.3255),
    "KOTA": (25.2138, 75.8648),
    "PUNE": (18.5204, 73.8567),
    "NZM": (28.5916, 77.2507),
    "SGNR": (29.9038, 73.8772),
    "RNC": (23.3432, 85.3096),
    "MFP": (26.1232, 85.3906),
    "BBS": (20.2961, 85.8245),
    "ALD": (25.4358, 81.8463),
    "MAQ": (12.8693, 74.8421),
    "ERS": (9.9946, 76.2999),
    "RMM": (9.2886, 79.3129),
    "TEN": (8.7274, 77.6845),
    "TVM": (8.5241, 76.9366),
    "JSME": (24.8202, 86.3380),
    "UAM": (11.4086, 76.7032),
    "KTE": (24.8436, 80.7998),
    "REWA": (24.5307, 81.3018),
    "GNT": (16.3067, 80.4365),
    "MDU": (9.9252, 78.1198),
    "CBE": (11.0168, 76.9558),
    "JAT": (32.7266, 74.8570),
    "SEE": (25.7186, 85.1839),
    "MB": (28.8389, 78.7768),
    "FZR": (30.9252, 74.6132),
    "SRE": (29.9640, 77.5460),
    "SVDK": (32.9910, 74.9495),
    "GADJ": (26.0870, 84.4320),
    "MGS": (25.3782, 83.5981)
    }

    # 👇 Now safe to use station_coords
    station_markers = [
        {"lat": lat, "lng": lng, "label": code}
        for code, (lat, lng) in station_coords.items()
    ]

    # Draw limited railway edges for clarity
    filtered_edges = [
        edge for edge in graph_data["edges"]
        if edge["source"] in station_coords and edge["destination"] in station_coords
    ][:15]  # Reduce to 15 edges for clear display

    railway_edges = []
    for edge in filtered_edges:
        try:
            from_lat, from_lng = station_coords[edge["source"]]
            to_lat, to_lng = station_coords[edge["destination"]]
            railway_edges.append({
                "source": {"lat": from_lat, "lng": from_lng},
                "destination": {"lat": to_lat, "lng": to_lng},
                "color": "#FF0000" if edge.get("congested") else "#0000FF"
            })
        except KeyError as e:
            print(f"🚫 Missing station in coordinates: {e}")
            continue

    return render_template("home.html",
                           congestion_points=congestion_points,
                           railway_edges=railway_edges,
                           station_markers=station_markers)
    
class RailwayNetwork:
    def __init__(self):
        self.graph = {
            'Delhi': {'Kanpur': 7, 'Lucknow': 6},
            'Kanpur': {'Delhi': 7, 'Bhopal': 9},
            'Lucknow': {'Delhi': 6, 'Varanasi': 5},
            'Bhopal': {'Kanpur': 9, 'Nagpur': 8},
            'Varanasi': {'Lucknow': 5, 'Patna': 4},
            'Nagpur': {'Bhopal': 8, 'Hyderabad': 10},
            'Patna': {'Varanasi': 4},
            'Hyderabad': {'Nagpur': 10}
        }

    def get_graph(self):
        return self.graph

    def shortest_path(self, start, end):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        pq = [(0, start)]
        previous = {}

        while pq:
            current_dist, current_node = heapq.heappop(pq)
            if current_node == end:
                break

            for neighbor, weight in self.graph[current_node].items():
                distance = current_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))

        path = []
        curr = end
        while curr in previous:
            path.insert(0, curr)
            curr = previous[curr]
        if path:
            path.insert(0, curr)
        return path, distances[end] if distances[end] != float('inf') else None

@app.route("/live_status", methods=["POST"])
def live_status():
    train_number = request.form["train_number"]
    start_day = request.form["start_day"]
    result = api_requests.get_live_status(train_number, start_day)

    print("🚆 Live Status API response:", result)
    status = result.get("data", {}).get("position", "N/A") if isinstance(result, dict) else "Invalid format"
    print("✅ Extracted status:", status)

    return render_template("home.html", live_status_result=status)

@app.route("/seat_availability", methods=["POST"])
def seat_availability():
    train_no = request.form["train_no"]
    source = request.form["source"]
    destination = request.form["destination"]
    date = request.form["date"]
    quota = request.form["quota"]
    cls = request.form["cls"]
    result = api_requests.get_seat_availability(train_no, source, destination, date, cls, quota)
    return render_template("home.html", seat_availability_result=result)

@app.route("/search_train_form", methods=["POST"])
def search_train():
    query = request.form["train"]
    result = api_requests.search_train(query)
    if not result or "data" not in result:
        result = {"data": []}
    return render_template("home.html", train_search_result=result)

@app.route("/search_station_form", methods=["POST"])
def search_station_form():
    query = request.form["station"]
    result = api_requests.search_station(query)
    return render_template("home.html", station_search_result=result)

@app.route("/autocomplete/train")
def autocomplete_train():
    query = request.args.get("term", "")
    res = api_requests.search_train(query)
    return jsonify([f"{item.get('train_number')} - {item.get('train_name')}" for item in res.get("data", [])])

@app.route("/autocomplete/station")
def autocomplete_station():
    query = request.args.get("term", "")
    res = api_requests.search_station(query)
    return jsonify([f"{item.get('station', {}).get('code')} - {item.get('station', {}).get('name')}" for item in res.get("data", [])])

@app.route("/train_schedule", methods=["POST"])
def train_schedule():
    train_number = request.form["train_number"]
    result = api_requests.get_train_schedule(train_number)
    return render_template("home.html", train_schedule_result=result)

@app.route("/shortest_path", methods=["POST"])
def shortest_path():
    source = request.form["source"]
    destination = request.form["destination"]
    graph_data = load_graph("railway_graph.json")
    graph = build_adjacency_list(graph_data)
    distances, predecessors = bellman_ford(graph, source)

    if distances.get(destination) == float('inf'):
        result = f"No path from {source} to {destination}"
    else:
        path = []
        current = destination
        while current != source:
            path.append(current)
            current = predecessors.get(current)
            if current is None:
                result = f"Path construction failed from {source} to {destination}"
                return render_template("home.html", shortest_path_result=result)
        path.append(source)
        path.reverse()
        result = {
            "distance": distances[destination],
            "path": path
        }

    return render_template("home.html", shortest_path_result=result)

@app.route("/max_flow", methods=["POST"])
def max_flow():
    source = request.form["source"]
    destination = request.form["destination"]
    graph_data = load_graph("railway_graph.json")
    graph = build_adjacency_list(graph_data)

    try:
        max_flow_value = ford_fulkerson(graph, source, destination)
        result = f"Maximum flow from {source} to {destination} is {max_flow_value}"
    except Exception as e:
        result = f"Error: {str(e)}"

    return render_template("home.html", max_flow_result=result)

@app.route("/congestion_map")
def congestion_map():
    congestion_data = [
         {"station": "NDLS", "name": "New Delhi", "lat": 28.6139, "lon": 77.2090, "congestion": 0.9},
        {"station": "BCT", "name": "Mumbai Central", "lat": 18.9696, "lon": 72.8195, "congestion": 0.6},
        {"station": "HWH", "name": "Howrah", "lat": 22.5806, "lon": 88.3495, "congestion": 0.3},
        {"station": "BJU", "name": "Barauni", "lat": 25.4753, "lon": 86.0030, "congestion": 0.7},
        {"station": "CNB", "name": "Kanpur", "lat": 26.4499, "lon": 80.3319, "congestion": 0.8},
        {"station": "LKO", "name": "Lucknow", "lat": 26.8467, "lon": 80.9462, "congestion": 0.75},
        {"station": "SBC", "name": "Bengaluru", "lat": 12.9784, "lon": 77.5695, "congestion": 0.65},
        {"station": "MAS", "name": "Chennai", "lat": 13.0827, "lon": 80.2707, "congestion": 0.4},
        {"station": "PUNE", "name": "Pune", "lat": 18.5204, "lon": 73.8567, "congestion": 0.55},
        {"station": "GKP", "name": "Gorakhpur", "lat": 26.7606, "lon": 83.3732, "congestion": 0.45},
        {"station": "CSTM", "name": "Mumbai CST", "lat": 18.9401, "lon": 72.8355, "congestion": 0.7},
        {"station": "ERS", "name": "Ernakulam", "lat": 9.9946, "lon": 76.2999, "congestion": 0.6},
        {"station": "TVM", "name": "Trivandrum", "lat": 8.5241, "lon": 76.9366, "congestion": 0.5},
        {"station": "MDU", "name": "Madurai", "lat": 9.9252, "lon": 78.1198, "congestion": 0.8},
        {"station": "JBP", "name": "Jabalpur", "lat": 23.1815, "lon": 79.9864, "congestion": 0.6},
        {"station": "ET", "name": "Itarsi", "lat": 22.6526, "lon": 78.7594, "congestion": 0.65},
        {"station": "GAYA", "name": "Gaya", "lat": 24.7969, "lon": 85.0002, "congestion": 0.85},
        {"station": "BSB", "name": "Varanasi", "lat": 25.3176, "lon": 82.9739, "congestion": 0.9},
        {"station": "SEE", "name": "Sonpur", "lat": 25.7186, "lon": 85.1839, "congestion": 0.7},
        {"station": "DNR", "name": "Danapur", "lat": 25.5941, "lon": 85.1376, "congestion": 0.6},
        {"station": "GHY", "name": "GUWAHATI", "lat": 26.1020, "lon": 91.4445, "congestion": 0.6},
    ]
    return render_template("congestion_map.html", data=congestion_data)

if __name__ == "__main__":
    app.run(debug=True)