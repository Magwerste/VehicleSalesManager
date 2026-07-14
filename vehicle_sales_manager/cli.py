"""Interactive console interface for the vehicle sales manager.

VehicleSalesApp owns the menu loop and all input/output. It delegates
every piece of business logic (validation, storage, searching) to the
model and repository layers, so this module only deals with prompting
the user and formatting responses.
"""

from pathlib import Path

from .enums import Branch, VehicleType
from .exceptions import DuplicateVehicleError, VehicleNotFoundError
from .models import Car, Minibus, Van, Vehicle
from .repository import VehicleRepository

DEFAULT_STORAGE_PATH = Path("vehicles.json")


class VehicleSalesApp:
    """The interactive menu-driven console application."""

    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    @classmethod
    def with_default_storage(cls) -> "VehicleSalesApp":
        return cls(VehicleRepository(DEFAULT_STORAGE_PATH))

    def run(self) -> None:
        self.repository.load()
        menu_actions = {
            "1": self.add_vehicle,
            "2": self.view_vehicles,
            "3": self.search_vehicles,
            "4": self.make_offer,
        }

        while True:
            print("\nUWS Vehicle Sales\n")
            print("1. Add Vehicle")
            print("2. View Vehicles")
            print("3. Search Vehicles")
            print("4. Make Offer")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ").strip()
            if choice == "5":
                self.repository.save()
                break

            action = menu_actions.get(choice)
            if action is None:
                print("Invalid choice. Please try again.")
                continue

            action()

        print("Thank you for using UWS Vehicle Sales!")

    # --- Menu actions ------------------------------------------------------

    def add_vehicle(self) -> None:
        print("\nAdd New Vehicle\n")
        try:
            vehicle_type = VehicleType.from_string(
                input("Enter vehicle type (Car/Van/Minibus): ")
            )
        except ValueError as error:
            print(error)
            return

        try:
            reg_num = input("Enter registration number (e.g. AB12CDE): ")
            make = input("Enter make (e.g., Ford, Toyota): ")
            model = input("Enter model (e.g., Fiesta, Corolla): ")
            colour = input("Enter colour (e.g., Red, Blue): ")
            price = float(input("Enter selling price (e.g., 10000.00): "))
            cost = float(input("Enter cost (e.g., 8000.00): "))
            branch = self._prompt_branch()
            vehicle = self._build_vehicle(vehicle_type, reg_num, make, model, colour, price, cost, branch)
            self.repository.add(vehicle)
            print(f"Added {vehicle.vehicle_type.lower()} {vehicle.reg_num} to stock.")
        except (ValueError, DuplicateVehicleError) as error:
            print(f"Error: {error}")

    def _prompt_branch(self) -> Branch:
        while True:
            try:
                return Branch.from_string(input("Enter branch (Mail/Add/Sand/Temple): "))
            except ValueError as error:
                print(error)

    def _build_vehicle(
        self,
        vehicle_type: VehicleType,
        reg_num: str,
        make: str,
        model: str,
        colour: str,
        price: float,
        cost: float,
        branch: Branch,
    ) -> Vehicle:
        if vehicle_type is VehicleType.CAR:
            doors = int(input("Enter number of doors (e.g., 2, 4): "))
            return Car(reg_num, make, model, colour, price, cost, branch, doors)
        if vehicle_type is VehicleType.VAN:
            capacity = float(input("Enter capacity in kg (e.g., 1000.0): "))
            return Van(reg_num, make, model, colour, price, cost, branch, capacity)
        seats = int(input("Enter number of seats (e.g., 12, 16): "))
        return Minibus(reg_num, make, model, colour, price, cost, branch, seats)

    def view_vehicles(self) -> None:
        print("\nAll Vehicles\n")
        vehicles = self.repository.all()
        if not vehicles:
            print("No vehicles in stock.")
            return
        for vehicle in vehicles:
            print(vehicle.get_details())

    def search_vehicles(self) -> None:
        print("\nSearch Vehicles\n")
        criteria = input(
            "Enter search criteria (Registration/Type/Make/Model/Colour/Price Range/Branch): "
        ).strip().lower()

        handlers = {
            "registration": self._search_by_registration,
            "type": self._search_by_type,
            "make": lambda: self._print_results(self.repository.find_by_make(input("Enter make: "))),
            "model": lambda: self._print_results(self.repository.find_by_model(input("Enter model: "))),
            "colour": lambda: self._print_results(self.repository.find_by_colour(input("Enter colour: "))),
            "price range": self._search_by_price_range,
            "branch": self._search_by_branch,
        }

        handler = handlers.get(criteria)
        if handler is None:
            print("Invalid search criteria!")
            return
        handler()

    def _search_by_registration(self) -> None:
        reg_num = input("Enter registration number (e.g. AB12CDE): ")
        try:
            print(self.repository.get(reg_num).get_details())
        except VehicleNotFoundError as error:
            print(error)

    def _search_by_type(self) -> None:
        try:
            vehicle_type = VehicleType.from_string(input("Enter vehicle type (Car/Van/Minibus): "))
        except ValueError as error:
            print(error)
            return
        self._print_results(
            self.repository.find_by_type(vehicle_type),
            not_found_message=f"No {vehicle_type.value.lower()}s found.",
        )

    def _search_by_price_range(self) -> None:
        try:
            minimum = float(input("Enter minimum price: "))
            maximum = float(input("Enter maximum price: "))
        except ValueError:
            print("Error: Invalid price input. Please enter a valid number.")
            return
        self._print_results(
            self.repository.find_by_price_range(minimum, maximum),
            not_found_message=f"No vehicles found within the price range £{minimum} - £{maximum}.",
        )

    def _search_by_branch(self) -> None:
        branch = self._prompt_branch()
        self._print_results(
            self.repository.find_by_branch(branch),
            not_found_message=f"No vehicles found at the {branch.value} branch.",
        )

    def _print_results(self, vehicles: list, not_found_message: str = "No vehicles found.") -> None:
        if not vehicles:
            print(not_found_message)
            return
        for vehicle in vehicles:
            print(vehicle.get_details())

    def make_offer(self) -> None:
        print("\nMake Offer\n")
        reg_num = input("Enter registration number (e.g. AB12CDE): ")
        try:
            vehicle = self.repository.get(reg_num)
        except VehicleNotFoundError as error:
            print(error)
            return

        try:
            offer = float(input(f"Enter your offer for {vehicle.make} {vehicle.model}: "))
        except ValueError:
            print("Error: Invalid offer input. Please enter a valid number.")
            return

        if offer >= vehicle.cost * 1.5:
            print(f"Offer of £{offer:.2f} accepted for {vehicle.make} {vehicle.model}!")
            self.repository.remove(vehicle.reg_num)
        else:
            print(f"Offer of £{offer:.2f} is too low for {vehicle.make} {vehicle.model}.")
