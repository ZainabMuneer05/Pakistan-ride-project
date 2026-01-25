import random

def service(distance, vehicle):
    rate = 10 if vehicle == "Bike" else 25 if vehicle == "Mini" else 45
    surge = random.choice([1.0, 1.2, 1.5])
    return distance * rate * surge, surge