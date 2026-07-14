import tempfile
import unittest
from pathlib import Path

from vehicle_sales_manager.enums import Branch, VehicleType
from vehicle_sales_manager.exceptions import DuplicateVehicleError, VehicleNotFoundError
from vehicle_sales_manager.models import Car, Van
from vehicle_sales_manager.repository import VehicleRepository


class TestVehicleRepository(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "vehicles.json"
        self.repository = VehicleRepository(self.storage_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_get_round_trip(self):
        car = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)
        self.repository.add(car)
        self.assertEqual(self.repository.get("ab12cde"), car)

    def test_add_duplicate_raises(self):
        car = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)
        self.repository.add(car)
        with self.assertRaises(DuplicateVehicleError):
            self.repository.add(car)

    def test_get_missing_raises(self):
        with self.assertRaises(VehicleNotFoundError):
            self.repository.get("ZZ99ZZZ")

    def test_remove_deletes_vehicle(self):
        car = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)
        self.repository.add(car)
        self.repository.remove("AB12CDE")
        self.assertEqual(len(self.repository), 0)

    def test_save_and_load_round_trip(self):
        self.repository.add(Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4))
        self.repository.add(Van("XY34FGH", "Ford", "Transit", "White", 15000, 12000, Branch.SAND, 1200.0))
        self.repository.save()

        reloaded = VehicleRepository(self.storage_path)
        reloaded.load()
        self.assertEqual(len(reloaded), 2)
        self.assertEqual(reloaded.get("AB12CDE").make, "Ford")

    def test_load_missing_file_is_empty(self):
        self.repository.load()
        self.assertEqual(len(self.repository), 0)

    def test_find_by_price_range(self):
        self.repository.add(Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4))
        self.repository.add(Car("XY34FGH", "Toyota", "Corolla", "Blue", 20000, 16000, Branch.SAND, 4))
        results = self.repository.find_by_price_range(15000, 25000)
        self.assertEqual([v.reg_num for v in results], ["XY34FGH"])

    def test_find_by_type(self):
        self.repository.add(Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4))
        self.repository.add(Van("XY34FGH", "Ford", "Transit", "White", 15000, 12000, Branch.SAND, 1200.0))
        results = self.repository.find_by_type(VehicleType.VAN)
        self.assertEqual([v.reg_num for v in results], ["XY34FGH"])


if __name__ == "__main__":
    unittest.main()
