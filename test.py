import requests

BASE = "http://10.0.0.9:5000"

dummy_data = [
    {"Username": "Roy", "Password": "1234", "Name": "roy waldman", },
    {"Username": "Yuval", "Password": "1234", "Name": "yuval cohen", },
]
# for user in dummy_data:
#     response = requests.put(f"{BASE}/users", user)
#     print(response.json())
# input()
d = f"{BASE}/users?Username=Roy&Password=1234"
print(d)
response = requests.get(f"{BASE}/users?Username=Roy&Password=1234")
print(response.json())
