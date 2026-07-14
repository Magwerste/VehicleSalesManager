"""Enumerations used across the vehicle sales manager."""

from enum import Enum


class Branch(Enum):
    """A dealership branch."""

    MAIL = "Mail"
    ADD = "Add"
    SAND = "Sand"
    TEMPLE = "Temple"

    @classmethod
    def from_string(cls, value: str) -> "Branch":
        """Resolve a branch from a case-insensitive name.

        Raises:
            ValueError: If no branch matches the given value.
        """
        normalised = value.strip().lower()
        for branch in cls:
            if branch.value.lower() == normalised:
                return branch
        valid = ", ".join(branch.value for branch in cls)
        raise ValueError(f"Unknown branch '{value}'. Valid branches: {valid}.")


class VehicleType(Enum):
    """The supported vehicle categories."""

    CAR = "Car"
    VAN = "Van"
    MINIBUS = "Minibus"

    @classmethod
    def from_string(cls, value: str) -> "VehicleType":
        """Resolve a vehicle type from a case-insensitive name.

        Raises:
            ValueError: If no vehicle type matches the given value.
        """
        normalised = value.strip().lower()
        for vehicle_type in cls:
            if vehicle_type.value.lower() == normalised:
                return vehicle_type
        valid = ", ".join(vehicle_type.value for vehicle_type in cls)
        raise ValueError(f"Unknown vehicle type '{value}'. Valid types: {valid}.")
