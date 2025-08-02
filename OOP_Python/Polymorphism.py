# Polymorfismus - práce se stejně různými formáty objektu stejným způsobem -> dvě různé třídy, ale používáme u obou stejnou věc
# a tím je ten print na konci

# Zadání:
# Spočítat předběžnou cenu zápujčky auta a dodávky
# Cena za půjčení vozu se ličí podle typu vozu, ujetých kilometrů a doby zapůjčení
class Car:
    price_base_loan = 200
    price_base_kilometers = 9 #CZK per kilometer

    @classmethod
    def calculatePrice(cls, kilometers, loan_period):
        final_price = kilometers * cls.price_base_kilometers + loan_period * cls.price_base_loan
        print(f"You can loan this car for {final_price} CZK.")

class Van:
    price_base_loan = 500
    price_base_kilometers = 14 #CZK per kilometer
    price_base_surcharge_per_day = 50

    @classmethod
    def calculatePrice(cls, kilometers, loan_period):
        final_price = kilometers * cls.price_base_kilometers + loan_period * cls.price_base_loan
        if (loan_period > 3):
            base_surcharge = cls.price_base_surcharge_per_day
            while (loan_period > 3):
                loan_period -= 1
                final_price += base_surcharge
                base_surcharge += cls.price_base_surcharge_per_day            
        print(f"You can loan this car for {final_price} CZK.")

vehicles = [Car(), Van()]

for vehicle in vehicles:
    vehicle.calculatePrice(0, 5)