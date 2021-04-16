import requests
from shared import BASE_URL

dummy_data = [
    {"Username": "Roy", "Password": "1234", "Name": "roy waldman", },
    {"Username": "Yuval", "Password": "1234", "Name": "yuval cohen", },
    {"Username": "Test1", "Password": "1234", "Name": "Test1", },
]

for user in dummy_data:
    response = requests.put(f"{BASE_URL}/users/", user)
    print(response.json())
# input()
d = f"{BASE_URL}/users?Username=Roy&Password=1234"
response = requests.get(d)
print(response.json())
