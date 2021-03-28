import requests

BASE = "http://127.0.0.1:5000"

dummy_data = [
    {'likes': 78, 'name': "joe", "views": 100000},
    {'likes': 3, 'name': "roy", "views": 456},
    {'likes': 100, 'name': "yuval", "views": 987},
    {'likes': 1, 'name': "tomer", "views": 1},
    {'likes': 2, 'name': "omry", "views": 2}
]

for i in range(len(dummy_data)):
    response = requests.put(f"{BASE}/video/{i}", dummy_data[i])
    print(response.json())
input()
response = requests.get(f"{BASE}/video/{2}")
print(response.json())
