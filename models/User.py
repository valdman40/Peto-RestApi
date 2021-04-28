class User:
    def __init__(self, username: str, id: int = None, name: str = None, password: str = None):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(name= {self.name}, username= {self.username},password= {self.password})"
