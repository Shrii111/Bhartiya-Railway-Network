from collections import defaultdict
import requests, json, time

API_BASE = "https://irctc1.p.rapidapi.com"
HEADERS = {
    "x-rapidapi-host": "irctc1.p.rapidapi.com",
    "x-rapidapi-key": "YOUR_API_KEY"  # Replace with your actual key
}

def get_train_numbers(letter):
    resp = requests.get(f"{API_BASE}/api/v1/searchTrain", headers=HEADERS, params={"query": letter})
    return [item["train_number"] for item in resp.json().get("data", [])]

def get_schedule(train_no):
    resp = requests.get(f"{API_BASE}/api/v1/getTrainSchedule", headers=HEADERS, params={"trainNo": train_no})
    return resp.json().get("data", {}).get("route", [])

def build_graph(trains):
    graph = defaultdict(dict)
    for t in trains:
        try:
            route = get_schedule(t)
            for i in range(len(route) - 1):
                u = route[i]["station_code"]
                v = route[i + 1]["station_code"]
                d1 = route[i]["distance"]
                d2 = route[i + 1]["distance"]
                dist = d2 - d1
                graph[u].setdefault(v, {"distance": 0, "capacity": 0})
                graph[u][v]["distance"] += dist
                graph[u][v]["capacity"] += 1
            time.sleep(0.2)  # throttle
        except Exception as e:
            print(f"Error for train {t}: {e}")
    return graph

if __name__ == "__main__":
    trains = set()
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        trains.update(get_train_numbers(ch))
        time.sleep(0.2)

    print(f"Fetched {len(trains)} trains")
    graph = build_graph(list(trains)[:500])  # Limit to first 500
    
    with open("railway_graph.json", "w") as f:
        json.dump(graph, f, indent=2)

    print("Saved to railway_graph.json")
