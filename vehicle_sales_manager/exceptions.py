"""Custom exceptions for the vehicle sales manager."""


class VehicleSalesError(Exception):
    """Base class for all domain-specific errors raised by this package."""


class DuplicateVehicleError(VehicleSalesError):
    """Raised when a vehicle with an already-registered registration number is added."""

    def __init__(self, reg_num: str):
        super().__init__(f"Vehicle with registration '{reg_num}' already exists.")
        self.reg_num = reg_num


class VehicleNotFoundError(VehicleSalesError):
    """Raised when a lookup by registration number finds no matching vehicle."""

    def __init__(self, reg_num: str):
        super().__init__(f"No vehicle found with registration '{reg_num}'.")
        self.reg_num = reg_num


class InvalidVehicleDataError(VehicleSalesError):
    """Raised when stored vehicle data cannot be reconstructed into a Vehicle."""
