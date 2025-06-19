import requests

API_HOST = "irctc1.p.rapidapi.com"
API_KEY = "b240b435e7mshd163ae3c3a56258p1d422fjsn2a122afd95a3"

HEADERS_V3 = {
    "x-rapidapi-host": API_HOST,
    "x-rapidapi-key": API_KEY
}

HEADERS_V1 = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

BASE_URL_V3 = f"https://{API_HOST}/api/v3"
BASE_URL_V1 = f"https://{API_HOST}/api/v1"
BASE_URL_V1 = "https://irctc1.p.rapidapi.com/api/v1"

def get_pnr_status(pnr_number):
    url = f"{BASE_URL_V3}/getPNRStatus?pnr={pnr_number}"
    return requests.get(url, headers=HEADERS_V3).json()

def get_train_schedule(train_number):
    url = f"{BASE_URL_V1}/getTrainSchedule"
    params = {"trainNo": train_number}
    response = requests.get(url, headers=HEADERS_V1, params=params)
    data = response.json()
    print("📅 Train Schedule API Response:", data)  # For debugging
    return data

def get_live_status(train_number, start_day):
    url = f"{BASE_URL_V1}/liveTrainStatus"
    params = {
        "trainNo": train_number,
        "startDay": start_day  # 0 = today, 1 = yesterday, 2 = day before, etc.
    }
    return requests.get(url, headers=HEADERS_V1, params=params).json()

def get_seat_availability(train_no, source, destination, date, cls, quota):
    url = "https://irctc1.p.rapidapi.com/api/v1/checkSeatAvailability"
    params = {
        "trainNo": train_no.strip(),
        "sourceStationCode": source.strip().upper(),
        "destStationCode": destination.strip().upper(),
        "date": date.strip(),  # dd-mm-yyyy
        "classCode": cls.strip().upper(),
        "quota": quota.strip().upper()
    }
    headers = {
        "x-rapidapi-host": "irctc1.p.rapidapi.com",
        "x-rapidapi-key": "486e57708dmsh8b7e1a6d16eb7c3p1297a2jsnbb5821ee6d11"
    }
    response = requests.get(url, headers=headers, params=params)
    print("🪑 Seat Availability API Response:", response.json())
    return response.json()




def get_live_station(station_code, hours):
    url = f"{BASE_URL_V3}/getLiveStation?stationCode={station_code}&hours={hours}"
    return requests.get(url, headers=HEADERS_V3).json()

def get_trains_by_station(station_code):
    url = f"{BASE_URL_V3}/getTrainsByStation?stationCode={station_code}"
    return requests.get(url, headers=HEADERS_V3).json()

def search_train(query):
    url = f"{BASE_URL_V1}/searchTrain"
    params = {"query": query}
    
    response = requests.get(url, headers=HEADERS_V1, params=params)
    data = response.json()
    
    print("🔍 API Response for search_train:", data)  # Debug line
    
    return data

def search_station(query):
    url = f"{BASE_URL_V1}/searchStation"
    params = {"query": query}
    response = requests.get(url, headers=HEADERS_V1, params=params)
    print("🔍 Station Search API Response:", response.json())  # for debugging
    return response.json()
