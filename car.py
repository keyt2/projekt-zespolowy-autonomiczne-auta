
class Car:
    def __init__(self, car_id: int, capacity: int, x: float, y: float, battery_time: int):
        self.car_id = car_id
        self.capacity = capacity
        self.x = x
        self.y = y
        self.battery_time = battery_time

    def show_statistics(self):
        print(f"Car number: {self.car_id}, capacity: {self.capacity} people, coordinates: ({self.x},{self.y}),"
              f" battery time left: {self.battery_time}")

