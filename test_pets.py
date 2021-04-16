import requests
from shared import BASE_URL

dummy_pets = [
    {"Name": "Tokyo", "Type": "dog", "User_Id": "1"},
    {"Name": "Luna", "Type": "Cat", "User_Id": "1"},
    {"Name": "Alpha", "Type": "Cat", "User_Id": "1"},
    {"Name": "Alpha1", "Type": "Cat", "User_Id": "1"},
    {"Name": "Alpha2", "Type": "Cat", "User_Id": "1"},
]
for pet in dummy_pets:
    response = requests.put(f"{BASE_URL}/pets/", pet)
    print(response.json())
response = requests.delete(f"{BASE_URL}/pets/{3}")
print(response.json())
