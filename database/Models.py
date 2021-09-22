class UserModel():
    def __init__(self, username: str, id: int = None, name: str = None, password: str = None):
        self.id = id
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f"User(name= {self.name}, username= {self.username},password= {self.password})"


class PetModel():
    def __init__(self, id: int = None, name: str = None, type: str = None, user_id: int = None):
        self.id = id
        self.name = name
        self.type = type
        self.user_id = user_id

    def __repr__(self):
        return f"Pet(name= {self.name}, type= {self.type}, user_id= {self.user_id})"


class MealsModel():
    def __init__(self, id: int = None, name: str = None, amount: int = None, time: str = None, repeat_daily: str = None,
                 pet_id: int = None):
        self.id = id
        self.name = name
        self.amount = amount
        self.time = time
        self.repeat_daily = repeat_daily
        self.pet_id = pet_id

    def __repr__(self):
        return f"Meal(id= {self.id}, name= {self.name}, amount= {self.amount},time= {self.time} ,type= {self.repeat_daily}, pet_id= {self.pet_id})"


class MealSummaryModel():
    def __init__(self, name: str = None, mealTime: str = None, petStartedEating: str = None, amountGiven: int = None,
                 amountEaten: int = None,
                 petFinishedEating: str = None):
        self.name = name
        self.mealTime = mealTime
        self.petStartedEating = petStartedEating
        self.amountGiven = amountGiven
        self.amountEaten = amountEaten
        self.petFinishedEating = petFinishedEating
