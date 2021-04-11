import requests

# BASE = "http://10.0.0.0:5000"
BASE = "http://192.168.43.72:5000"

dummy_data = [
    {"Username": "Roy", "Password": "1234", "Name": "roy waldman", },
    {"Username": "Yuval", "Password": "1234", "Name": "yuval cohen", },
    {"Username": "Test1", "Password": "1234", "Name": "Test1", },
]

for user in dummy_data:
    response = requests.put(f"{BASE}/users/", user)
    print(response.json())
# input()
d = f"{BASE}/users?Username=Roy&Password=1234"
print(d)
response = requests.get(f"{BASE}/users?Username=Roy&Password=1234")
print(response.json())
