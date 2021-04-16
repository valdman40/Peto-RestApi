import requests
from shared import BASE_URL

response = requests.get(f"{BASE_URL}/pets/user/{1}")
pets_of_user = response.json()
print("user pets:\n[")
for pet in pets_of_user:
    print(f"{pet},")
print("]")
