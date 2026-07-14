"""Vehicle Sales Manager: a small console application for managing vehicle stock."""

from .models import Car, Minibus, Van, Vehicle
from .repository import VehicleRepository

__all__ = ["Vehicle", "Car", "Van", "Minibus", "VehicleRepository"]
