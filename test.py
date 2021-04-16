import requests
from shared import BASE_URL

# dummy_data = [
#     {"Username": "Roy", "Password": "1234", "Name": "roy waldman", },
#     {"Username": "Yuval", "Password": "1234", "Name": "yuval cohen", },
#     {"Username": "Test1", "Password": "1234", "Name": "Test1", },
# ]
#
# for user in dummy_data:
#     response = requests.put(f"{BASE}/users/", user)
#     print(response.json())
# # input()
# d = f"{BASE}/users?Username=Roy&Password=1234"
# print(d)
# response = requests.get(f"{BASE}/users?Username=Roy&Password=1234")
# print(response.json())

# dummy_pets = [
#     {"Name": "Tokyo", "Type": "dog", "User_Id": "1"},
#     {"Name": "Luna", "Type": "Cat", "User_Id": "1"},
#     {"Name": "Alpha", "Type": "Cat", "User_Id": "1"},
#     {"Name": "Alpha1", "Type": "Cat", "User_Id": "1"},
#     {"Name": "Alpha2", "Type": "Cat", "User_Id": "1"},
# ]
# for pet in dummy_pets:
#     response = requests.put(f"{BASE}/pets/", pet)
#     print(response.json())
# response = requests.delete(f"{BASE}/pets/{3}")
# print(response.json())

response = requests.get(f"{BASE_URL}/pets/user/{1}")
pets_of_user = response.json()
print("user pets:\n[")
for pet in pets_of_user:
    print(f"{pet},")
print("]")
