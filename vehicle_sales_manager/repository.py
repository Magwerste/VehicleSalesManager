"""Persistence and querying for the vehicle stock.

VehicleRepository owns the in-memory collection of vehicles and is
responsible for loading from and saving to a JSON file on disk. Keeping
this separate from the CLI means the storage format can change without
touching any user-facing code, and the collection can be tested without
touching the filesystem.
"""

import json
from pathlib import Path
from typing import Iterator, List, Optional

from .enums import Branch, VehicleType
from .exceptions import DuplicateVehicleError, VehicleNotFoundError
from .models import Vehicle, vehicle_from_dict


class VehicleRepository:
    """An in-memory collection of vehicles, backed by a JSON file."""

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self._vehicles: dict[str, Vehicle] = {}

    def __len__(self) -> int:
        return len(self._vehicles)

    def __iter__(self) -> Iterator[Vehicle]:
        return iter(self._vehicles.values())

    def __contains__(self, reg_num: str) -> bool:
        return reg_num.strip().upper() in self._vehicles

    # --- Persistence ---------------------------------------------------------

    def load(self) -> None:
        """Load vehicles from the storage file, if it exists.

        A missing file is treated as an empty stock. A malformed file
        raises so the problem is visible rather than silently discarding data.
        """
        if not self.storage_path.exists():
            return

        with self.storage_path.open("r", encoding="utf-8") as file:
            raw_records = json.load(file)

        self._vehicles = {
            record["reg_num"]: vehicle_from_dict(record) for record in raw_records
        }

    def save(self) -> None:
        """Persist the current vehicle stock to the storage file."""
        records = [vehicle.to_dict() for vehicle in self._vehicles.values()]
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)

    # --- Mutation --------------------------------------------------------------

    def add(self, vehicle: Vehicle) -> None:
        """Add a vehicle to stock.

        Raises:
            DuplicateVehicleError: If a vehicle with the same registration
                number is already in stock.
        """
        if vehicle.reg_num in self._vehicles:
            raise DuplicateVehicleError(vehicle.reg_num)
        self._vehicles[vehicle.reg_num] = vehicle

    def remove(self, reg_num: str) -> Vehicle:
        """Remove and return the vehicle with the given registration number.

        Raises:
            VehicleNotFoundError: If no such vehicle is in stock.
        """
        key = reg_num.strip().upper()
        try:
            return self._vehicles.pop(key)
        except KeyError:
            raise VehicleNotFoundError(reg_num) from None

    def get(self, reg_num: str) -> Vehicle:
        """Return the vehicle with the given registration number.

        Raises:
            VehicleNotFoundError: If no such vehicle is in stock.
        """
        key = reg_num.strip().upper()
        try:
            return self._vehicles[key]
        except KeyError:
            raise VehicleNotFoundError(reg_num) from None

    # --- Queries -----------------------------------------------------------

    def all(self) -> List[Vehicle]:
        """Return every vehicle currently in stock."""
        return list(self._vehicles.values())

    def find_by_type(self, vehicle_type: VehicleType) -> List[Vehicle]:
        return [v for v in self._vehicles.values() if v.vehicle_type == vehicle_type.value]

    def find_by_make(self, make: str) -> List[Vehicle]:
        target = make.strip().title()
        return [v for v in self._vehicles.values() if v.make == target]

    def find_by_model(self, model: str) -> List[Vehicle]:
        target = model.strip().title()
        return [v for v in self._vehicles.values() if v.model == target]

    def find_by_colour(self, colour: str) -> List[Vehicle]:
        target = colour.strip().title()
        return [v for v in self._vehicles.values() if v.colour == target]

    def find_by_branch(self, branch: Branch) -> List[Vehicle]:
        return [v for v in self._vehicles.values() if v.branch == branch]

    def find_by_price_range(self, minimum: float, maximum: float) -> List[Vehicle]:
        return [v for v in self._vehicles.values() if minimum <= v.price <= maximum]

    def find_by_reg_num(self, reg_num: str) -> Optional[Vehicle]:
        return self._vehicles.get(reg_num.strip().upper())
