"""
Assignment1.py
DPIT121 - Assignment 1: Car Rental Management System (CLI)

This is a clean, single-file starter that fully meets the brief:
- FleetItem (base), Car (subclass), Customer, RentalAgency
- Command-line UI with 9 options
- Preloaded 5 cars + 5 customers for testing
- Simple, readable code with type hints and docstrings
- No heavy validation (per instructions)

You can run it with:  python3 Assignment1.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


# ---------- Domain Model ----------

@dataclass
class FleetItem:
    """Base class for all fleet items."""
    model_name: str


@dataclass
class Car(FleetItem):
    """Concrete vehicle type in the fleet."""
    car_id: int
    brand: str
    available: bool = True

    def __str__(self) -> str:
        status = "Available" if self.available else "Rented"
        return f"[{self.car_id}] {self.brand} {self.model_name} - {status}"


@dataclass
class Customer:
    """Represents a rental customer."""
    customer_id: int
    name: str
    rented_cars: List[Car] = field(default_factory=list)

    def __str__(self) -> str:
        rented_list = ", ".join(f"{c.brand} {c.model_name} (#{c.car_id})" for c in self.rented_cars) or "None"
        return f"[{self.customer_id}] {self.name} | Rented: {rented_list}"


class RentalAgency:
    """
    Manages the car fleet and the customer list.
    Responsibilities include searching, adding, renting, and returning cars.
    """
    def __init__(self) -> None:
        self.cars: List[Car] = []
        self.customers: List[Customer] = []
        self.next_car_id: int = 1  # auto-increment for new cars

    # ---- Fleet operations ----
    def show_fleet(self) -> None:
        print("\n--- Fleet ---")
        if not self.cars:
            print("No cars in the fleet yet.")
            return
        for car in self.cars:
            print(car)

    def add_car(self, brand: str, model_name: str) -> Car:
        car = Car(car_id=self.next_car_id, brand=brand, model_name=model_name, available=True)
        self.cars.append(car)
        self.next_car_id += 1
        return car

    def search_car_by_model(self, model_name: str) -> List[Car]:
        key = model_name.strip().lower()
        return [c for c in self.cars if key in c.model_name.lower()]

    def search_car_by_id(self, car_id: int) -> Optional[Car]:
        for c in self.cars:
            if c.car_id == car_id:
                return c
        return None

    # ---- Customer operations ----
    def show_customers(self) -> None:
        print("\n--- Customers ---")
        if not self.customers:
            print("No customers found.")
            return
        for cust in self.customers:
            print(cust)

    def add_customer(self, customer_id: int, name: str) -> Customer:
        # Simple uniqueness check (optional)
        if self.search_customer_by_id(customer_id) is not None:
            raise ValueError(f"Customer ID {customer_id} already exists.")
        cust = Customer(customer_id=customer_id, name=name)
        self.customers.append(cust)
        return cust

    def search_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        for cust in self.customers:
            if cust.customer_id == customer_id:
                return cust
        return None

    # ---- Rental operations ----
    def rent_car(self, customer_id: int, car_id: int) -> str:
        cust = self.search_customer_by_id(customer_id)
        if cust is None:
            return "Customer not found."

        car = self.search_car_by_id(car_id)
        if car is None:
            return "Car not found."

        if not car.available:
            return "Car is not available."

        car.available = False
        cust.rented_cars.append(car)
        return f"Car #{car.car_id} rented to {cust.name}."

    def return_car(self, customer_id: int, car_id: int) -> str:
        cust = self.search_customer_by_id(customer_id)
        if cust is None:
            return "Customer not found."

        car = self.search_car_by_id(car_id)
        if car is None:
            return "Car not found."

        # Ensure this customer actually has this car
        for i, c in enumerate(cust.rented_cars):
            if c.car_id == car_id:
                cust.rented_cars.pop(i)
                car.available = True
                return f"Car #{car.car_id} returned by {cust.name}."
        return "This customer did not rent that car."


# ---------- Seed/Test Data ----------

def seed_data(agency: RentalAgency) -> None:
    """Preload 5 cars and 5 customers for quick testing."""
    agency.add_car("Toyota", "Corolla")
    agency.add_car("Honda", "Civic")
    agency.add_car("BMW", "3 Series")
    agency.add_car("Audi", "A4")
    agency.add_car("Tesla", "Model 3")

    agency.add_customer(101, "Alice")
    agency.add_customer(102, "Bob")
    agency.add_customer(103, "Charlie")
    agency.add_customer(104, "Diana")
    agency.add_customer(105, "Ethan")


# ---------- CLI (Main Menu) ----------

def print_menu() -> None:
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


def main() -> None:
    agency = RentalAgency()
    seed_data(agency)  # preload

    while True:
        print_menu()
        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            agency.show_fleet()

        elif choice == "2":
            brand = input("Enter brand: ").strip()
            model = input("Enter model name: ").strip()
            car = agency.add_car(brand, model)
            print(f"Added car: {car}")

        elif choice == "3":
            q = input("Model name to search: ").strip()
            results = agency.search_car_by_model(q)
            if results:
                print("\nResults:")
                for car in results:
                    print(car)
            else:
                print("No cars matched your search.")

        elif choice == "4":
            agency.show_customers()

        elif choice == "5":
            try:
                cid = int(input("Enter new customer ID (int): ").strip())
                name = input("Enter customer name: ").strip()
                cust = agency.add_customer(cid, name)
                print(f"Added customer: {cust}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            try:
                cid = int(input("Enter customer ID to search: ").strip())
                cust = agency.search_customer_by_id(cid)
                if cust:
                    print(cust)
                else:
                    print("Customer not found.")
            except ValueError:
                print("Please enter a valid integer ID.")

        elif choice == "7":
            try:
                cid = int(input("Customer ID: ").strip())
                car_id = int(input("Car ID to rent: ").strip())
                msg = agency.rent_car(cid, car_id)
                print(msg)
            except ValueError:
                print("Please enter valid integer IDs.")

        elif choice == "8":
            try:
                cid = int(input("Customer ID: ").strip())
                car_id = int(input("Car ID to return: ").strip())
                msg = agency.return_car(cid, car_id)
                print(msg)
            except ValueError:
                print("Please enter valid integer IDs.")

        elif choice == "9":
            print("Exiting...")
            break

        else:
            print("Invalid option. Choose 1-9.")

        # small visual separator between actions
        print("\n---------------------------------------------------------\n")


if __name__ == "__main__":
    main()
