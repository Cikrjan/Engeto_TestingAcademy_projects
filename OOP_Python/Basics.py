# Rozdíl mezi Strukturovaným a obejktoě orientovaným programováním
# Strukturově
Cars = [
    {"brand": 'Audi', "consuption": 7},
    {"brand": 'Nissan', "consuption": 5},
    {"brand": 'Volvo', "consuption": 6}
]

Vans = [
    {"brand": 'Ford', "capacity": 14},
    {"brand": 'Mercedes-Benz', "capacity": 17}
]

def printCar(Car):
    print(f"Car of {Car['brand']} brand with consuption {Car['consuption']} l/100km")

def printVan(Van):
    print(f"Van of {Van['brand']} brand with capacity {Van['capacity']} m3")

for Car in Cars:
    printCar(Car)

for Van in Vans:
    printVan(Van)

# Objektově
class Car:
    def __init__(self, brand, consuption):
        self.brand = brand
        self.consuption = consuption

    def print(self) -> None:
        print(f"Car of {self.brand} brand with consuption {self.consuption} l/100km")

class Van:
    def __init__(self, brand, capacity):
        self.brand = brand
        self.capacity = capacity

    def print(self) -> None:
        print(f"Van of {self.brand} brand with capacity {self.capacity} m3")

vehicles = [
    Car('Audi', 7),
    Car('Nissan', 5),
    Car('Volvo', 6),
    Van('Ford', 14),
    Van('Mercedes-Benz', 17),
]

for vehicle in vehicles:
    vehicle.print()
