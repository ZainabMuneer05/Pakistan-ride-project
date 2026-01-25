import random

class Driver:
    def __init__(self, id, loc, vehicle):
        self.id = id
        self.location = loc
        self.vehicle = vehicle
        self.available = True
        self.earnings = 0
        self.rating = random.uniform(4.0, 5.0)