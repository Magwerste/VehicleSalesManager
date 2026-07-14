"""Domain models for vehicles held in stock.

Vehicle is an abstract base class; Car, Van and Minibus are concrete
subclasses that each add the attributes relevant to their category while
inheriting shared validation, formatting and serialisation behaviour.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Type

from .enums import Branch
from .exceptions import InvalidVehicleDataError


class Vehicle(ABC):
    """An abstract vehicle held in dealership stock.

    Subclasses must implement `vehicle_type` and `_extra_details` /
    `_extra_fields` to describe the attributes specific to that category.
    """

    def __init__(
        self,
        reg_num: str,
        make: str,
        model: str,
        colour: str,
        price: float,
        cost: float,
        branch: Branch,
    ):
        self.reg_num = reg_num
        self.make = make
        self.model = model
        self.colour = colour
        self.price = price
        self.cost = cost
        self.branch = branch

    # --- Validated properties -------------------------------------------------

    @property
    def reg_num(self) -> str:
        return self._reg_num

    @reg_num.setter
    def reg_num(self, value: str) -> None:
        cleaned = value.strip().upper()
        if not cleaned:
            raise ValueError("Registration number cannot be empty.")
        self._reg_num = cleaned

    @property
    def make(self) -> str:
        return self._make

    @make.setter
    def make(self, value: str) -> None:
        cleaned = value.strip().title()
        if not cleaned:
            raise ValueError("Make cannot be empty.")
        self._make = cleaned

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        cleaned = value.strip().title()
        if not cleaned:
            raise ValueError("Model cannot be empty.")
        self._model = cleaned

    @property
    def colour(self) -> str:
        return self._colour

    @colour.setter
    def colour(self, value: str) -> None:
        cleaned = value.strip().title()
        if not cleaned:
            raise ValueError("Colour cannot be empty.")
        self._colour = cleaned

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self._price = float(value)

    @property
    def cost(self) -> float:
        return self._cost

    @cost.setter
    def cost(self, value: float) -> None:
        if value < 0:
            raise ValueError("Cost cannot be negative.")
        self._cost = float(value)

    @property
    def branch(self) -> Branch:
        return self._branch

    @branch.setter
    def branch(self, value: Branch) -> None:
        if not isinstance(value, Branch):
            raise TypeError("branch must be a Branch enum member.")
        self._branch = value

    # --- Abstract interface -----------------------------------------------

    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """The human-readable category name, e.g. 'Car'."""

    @abstractmethod
    def _extra_fields(self) -> Dict[str, Any]:
        """Attributes specific to the subclass, keyed by attribute name."""

    # --- Shared behaviour ---------------------------------------------------

    def get_details(self) -> str:
        """Return a single-line human-readable summary of the vehicle."""
        base = (
            f"Registration: {self.reg_num}, Make: {self.make}, Model: {self.model}, "
            f"Colour: {self.colour}, Price: £{self.price:.2f}, Branch: {self.branch.value}"
        )
        extras = ", ".join(f"{label}: {value}" for label, value in self._extra_fields().items())
        return f"{base}, {extras}" if extras else base

    def to_dict(self) -> Dict[str, Any]:
        """Serialise this vehicle to a JSON-compatible dictionary."""
        data: Dict[str, Any] = {
            "vehicle_type": self.vehicle_type,
            "reg_num": self.reg_num,
            "make": self.make,
            "model": self.model,
            "colour": self.colour,
            "price": self.price,
            "cost": self.cost,
            "branch": self.branch.value,
        }
        data.update(self._subclass_data())
        return data

    def _subclass_data(self) -> Dict[str, Any]:
        """Raw constructor kwargs specific to the subclass, for serialisation."""
        return {key.lower(): value for key, value in self._extra_fields().items()}

    def __str__(self) -> str:
        return self.get_details()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(reg_num={self.reg_num!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.reg_num == other.reg_num

    def __hash__(self) -> int:
        return hash(self.reg_num)


class Car(Vehicle):
    """A car, additionally tracking its number of doors."""

    def __init__(
        self,
        reg_num: str,
        make: str,
        model: str,
        colour: str,
        price: float,
        cost: float,
        branch: Branch,
        doors: int,
    ):
        super().__init__(reg_num, make, model, colour, price, cost, branch)
        self.doors = doors

    @property
    def doors(self) -> int:
        return self._doors

    @doors.setter
    def doors(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Doors must be a positive integer.")
        self._doors = int(value)

    @property
    def vehicle_type(self) -> str:
        return "Car"

    def _extra_fields(self) -> Dict[str, Any]:
        return {"Doors": self.doors}


class Van(Vehicle):
    """A van, additionally tracking its load capacity in kilograms."""

    def __init__(
        self,
        reg_num: str,
        make: str,
        model: str,
        colour: str,
        price: float,
        cost: float,
        branch: Branch,
        capacity: float,
    ):
        super().__init__(reg_num, make, model, colour, price, cost, branch)
        self.capacity = capacity

    @property
    def capacity(self) -> float:
        return self._capacity

    @capacity.setter
    def capacity(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Capacity must be a positive number.")
        self._capacity = float(value)

    @property
    def vehicle_type(self) -> str:
        return "Van"

    def _extra_fields(self) -> Dict[str, Any]:
        return {"Capacity": f"{self.capacity}kg"}

    def _subclass_data(self) -> Dict[str, Any]:
        return {"capacity": self.capacity}


class Minibus(Vehicle):
    """A minibus, additionally tracking its seating capacity."""

    def __init__(
        self,
        reg_num: str,
        make: str,
        model: str,
        colour: str,
        price: float,
        cost: float,
        branch: Branch,
        seats: int,
    ):
        super().__init__(reg_num, make, model, colour, price, cost, branch)
        self.seats = seats

    @property
    def seats(self) -> int:
        return self._seats

    @seats.setter
    def seats(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Seats must be a positive integer.")
        self._seats = int(value)

    @property
    def vehicle_type(self) -> str:
        return "Minibus"

    def _extra_fields(self) -> Dict[str, Any]:
        return {"Seats": self.seats}


VEHICLE_CLASSES: Dict[str, Type[Vehicle]] = {
    "Car": Car,
    "Van": Van,
    "Minibus": Minibus,
}


def vehicle_from_dict(data: Dict[str, Any]) -> Vehicle:
    """Reconstruct a Vehicle subclass instance from a serialised dictionary.

    Raises:
        InvalidVehicleDataError: If the data is missing fields or references
            an unknown vehicle type.
    """
    try:
        vehicle_type = data["vehicle_type"]
        vehicle_class = VEHICLE_CLASSES[vehicle_type]
        branch = Branch.from_string(data["branch"])
        kwargs = {
            "reg_num": data["reg_num"],
            "make": data["make"],
            "model": data["model"],
            "colour": data["colour"],
            "price": data["price"],
            "cost": data["cost"],
            "branch": branch,
        }
        if vehicle_class is Car:
            kwargs["doors"] = data["doors"]
        elif vehicle_class is Van:
            kwargs["capacity"] = data["capacity"]
        elif vehicle_class is Minibus:
            kwargs["seats"] = data["seats"]
        return vehicle_class(**kwargs)
    except KeyError as error:
        raise InvalidVehicleDataError(f"Missing field {error} in stored vehicle data.") from error
