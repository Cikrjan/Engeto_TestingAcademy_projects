class SmartFridge: #Třída

    fridge_count = 0 #Třídní atribut
    temperatuer = 0

    def __init__(self, brand, model, voltage, power_consumption, number_of_hours): #Metoda __init__() -> tzv. konstruktor, který je vždy první a má povinný jeden paramter "self"
        self.brand = brand #Instanční atribut
        self.model = model #Instanční atribut
        self.voltage = voltage
        self.power_consumption = power_consumption
        self.number_of_hours = number_of_hours
        SmartFridge.fridge_count += 1 

    def greet(self): #Metoda
        print(f"Hello from {self.brand} {self.model}")

    @classmethod
    def final_fridge_count(cls):
        print(f"Total number of fridges is: {cls.fridge_count}")

    def compatibility_check(self):
        if  self.voltage == 230:
            return "✅ Compatible"
        else:
            return "❌ Not Compatible"

    def year_consumption(self):
        year_consumption = (self.power_consumption / 1000) * (self.number_of_hours * 365)
        return year_consumption
    
    def temperature(self):
        pass


fridges = {"Bosh": ("KGN56HI3P", 230, 10, 8), 
           "LG": ("GSX961NSAZ", 170, 8, 8)
           }

for brand, (model, voltage, power_consumption, number_of_hours) in fridges.items():
    fridge = SmartFridge(brand, model, voltage, power_consumption, number_of_hours)
    fridge.greet()
    print(f"Fridge {fridge.brand}, model: {fridge.model}, {fridge.compatibility_check()}, yearly consumption: {fridge.year_consumption():.2f} kWh")
    # SmartFridge.compatibility_check(voltage)

SmartFridge.final_fridge_count()
