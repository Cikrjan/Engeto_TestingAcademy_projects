# #Příklad s getter, setter a property

# class Car:
#     def __init__(self, brand, consuption):
#         self._brand = brand
#         self._consuption = consuption

#     def get_brand(self):
#         return self._brand
    
#     def set_brand(self, new_brand):
#         if not new_brand:
#             raise ValueError("You haven't entered brand")
#         self._brand = new_brand
    
# car = Car("škoda", 10)

# print(car.get_brand())

# car.set_brand("Nissan")
# print(car.get_brand())

# #Příklad s dekorátorem bez setteru tzn. Read-Only
# class Car:
#     def __init__(self, brand, consumption):
#         self._brand = brand
#         self._consumption = consumption
    
#     @property
#     def brand(self):
#         return self._brand
    
#     @property
#     def consumption(self):
#         return self._consumption
    
#     def print(self):
#         print(f"Car of {self._brand} brand has consumption {self._consumption} l/100km")
    
# car = Car("Škoda", 10)

# car.print()

# Cvičení
class Student:
    def __init__(self, name, grade):
        self._name = name
        self._grade = grade

    @property
    def name(self):
        return self._name
    
    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, grade):
        if not (1 <= grade <= 5):
            raise ValueError("Out of scale!")
        self._grade = grade

    def info(self):
        print(f"Student {self._name} has grade {self._grade}")

student = Student("Anna", 1)

student.info()

student.grade = 10
student.info()