class UserModel():
    def __init__(self, id: int, name: str, username: str, password: str):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(name= {self.name}, username= {self.username},password= {self.password})"


class PetModel():
    def __init__(self, id: int, name: str, type: str, user_id: int):
        self.id = id
        self.name = name
        self.type = type
        self.user_id = user_id

    def __repr__(self):
        return f"Pet(name= {self.name}, type= {self.type}, user_id= {self.user_id})"
