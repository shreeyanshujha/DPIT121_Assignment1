"""
Assignment1.py
DPIT121 Assignment 1 - Car Rental Management System
Single-file program with 4 classes + CLI menu.

Uses only Week 1-4 style Python OOP:
- normal classes
- __init__
- lists
- simple methods
- basic inheritance (required by assignment)
"""

# Classes

class FleetItem:
    # Base (super) class
    def __init__(self, model_name):
        self.model_name = model_name


class Car(FleetItem):
    # Subclass of FleetItem 
    def __init__(self, car_id, brand, model_name):
        FleetItem.__init__(self, model_name)   
        self.car_id = car_id
        self.brand = brand
        self.available = True  

    def __str__(self):
        if self.available:
            status = "Available"
        else:
            status = "Rented"
        return "[" + str(self.car_id) + "] " + self.brand + " " + self.model_name + " - " + status


class Customer:
    def __init__(self, customer_id, name):
        self.customer_id = customer_id
        self.name = name
        self.rented_cars = []  # list of Car objects

    def __str__(self):
        if len(self.rented_cars) == 0:
            rented_list = "None"
        else:
            rented_list = ""
            for c in self.rented_cars:
                rented_list += c.brand + " " + c.model_name + " (#" + str(c.car_id) + "), "
            rented_list = rented_list[:-2]  # remove last comma/space
        return "[" + str(self.customer_id) + "] " + self.name + " | Rented: " + rented_list


class RentalAgency:
    def __init__(self):
        self.cars = []
        self.customers = []
        self.next_car_id = 1

    # Fleet methods
    def show_fleet(self):
        print("\n--- Fleet ---")
        if len(self.cars) == 0:
            print("No cars in the fleet.")
            return
        for car in self.cars:
            print(car)

    def add_car(self, brand, model_name):
        car = Car(self.next_car_id, brand, model_name)
        self.cars.append(car)
        self.next_car_id += 1
        return car

    def search_car_by_model(self, model_name):
        results = []
        key = model_name.lower()
        for car in self.cars:
            if key in car.model_name.lower():
                results.append(car)
        return results

    def search_car_by_id(self, car_id):
        for car in self.cars:
            if car.car_id == car_id:
                return car
        return None

    # Customer methods 
    def show_customers(self):
        print("\n--- Customers ---")
        if len(self.customers) == 0:
            print("No customers found.")
            return
        for cust in self.customers:
            print(cust)

    def add_customer(self, customer_id, name):
        cust = Customer(customer_id, name)
        self.customers.append(cust)
        return cust

    def search_customer_by_id(self, customer_id):
        for cust in self.customers:
            if cust.customer_id == customer_id:
                return cust
        return None

    # Rent / return 
    def rent_car(self, customer_id, car_id):
        cust = self.search_customer_by_id(customer_id)
        if cust is None:
            return "Customer not found."

        car = self.search_car_by_id(car_id)
        if car is None:
            return "Car not found."

        if car.available == False:
            return "Car is not available."

        car.available = False
        cust.rented_cars.append(car)
        return "Car #" + str(car.car_id) + " rented to " + cust.name + "."

    def return_car(self, customer_id, car_id):
        cust = self.search_customer_by_id(customer_id)
        if cust is None:
            return "Customer not found."

        car = self.search_car_by_id(car_id)
        if car is None:
            return "Car not found."

        # find car inside customer's rented list
        for i in range(len(cust.rented_cars)):
            if cust.rented_cars[i].car_id == car_id:
                cust.rented_cars.pop(i)
                car.available = True
                return "Car #" + str(car.car_id) + " returned by " + cust.name + "."

        return "This customer did not rent that car."


#  Helper functions 

def seed_data(agency):
    # 5 cars
    agency.add_car("Toyota", "GR Corolla")
    agency.add_car("Honda", "Civic Type R")
    agency.add_car("BMW", "M3 Competition")
    agency.add_car("Audi", "RS5 Sportback")
    agency.add_car("Tesla", "Model 3 Performance")

    # 5 customers
    agency.add_customer(101, "Alice")
    agency.add_customer(102, "Bob")
    agency.add_customer(103, "Charlie")
    agency.add_customer(104, "Diana")
    agency.add_customer(105, "Ethan")


def print_menu():
    print("""
================= Car Rental Management =================
1) Show fleet
2) Add car
3) Search car by model name
4) Show list of current customers
5) Add new customer
6) Search customer by ID
7) Rent a car
8) Return a car
9) Exit
=========================================================
""")


# Main program 

def main():
    agency = RentalAgency()
    seed_data(agency)

    while True:
        print_menu()
        choice = input("Choose an option (1-9): ")

        if choice == "1":
            agency.show_fleet()

        elif choice == "2":
            brand = input("Enter brand: ")
            model = input("Enter model name: ")
            new_car = agency.add_car(brand, model)
            print("Added car:", new_car)

        elif choice == "3":
            model = input("Enter model name to search: ")
            results = agency.search_car_by_model(model)
            if len(results) == 0:
                print("No cars matched that model name.")
            else:
                print("\nSearch results:")
                for car in results:
                    print(car)

        elif choice == "4":
            agency.show_customers()

        elif choice == "5":
            cid = int(input("Enter new customer ID: "))
            name = input("Enter customer name: ")
            cust = agency.add_customer(cid, name)
            print("Added customer:", cust)

        elif choice == "6":
            cid = int(input("Enter customer ID to search: "))
            cust = agency.search_customer_by_id(cid)
            if cust is None:
                print("Customer not found.")
            else:
                print(cust)

        elif choice == "7":
            cid = int(input("Customer ID: "))
            car_id = int(input("Car ID to rent: "))
            print(agency.rent_car(cid, car_id))

        elif choice == "8":
            cid = int(input("Customer ID: "))
            car_id = int(input("Car ID to return: "))
            print(agency.return_car(cid, car_id))

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select 1-9.")

        print("\n-------------------------------------------------\n")


if __name__ == "__main__":
    main()

