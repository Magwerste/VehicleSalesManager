import unittest

from vehicle_sales_manager.enums import Branch
from vehicle_sales_manager.exceptions import InvalidVehicleDataError
from vehicle_sales_manager.models import Car, Minibus, Van, vehicle_from_dict


class TestVehicleValidation(unittest.TestCase):
    def test_fields_are_normalised(self):
        car = Car("ab12cde", "  ford ", "fiesta", "red", 10000, 8000, Branch.MAIL, 4)
        self.assertEqual(car.reg_num, "AB12CDE")
        self.assertEqual(car.make, "Ford")
        self.assertEqual(car.model, "Fiesta")
        self.assertEqual(car.colour, "Red")

    def test_negative_price_is_rejected(self):
        with self.assertRaises(ValueError):
            Car("AB12CDE", "Ford", "Fiesta", "Red", -1, 8000, Branch.MAIL, 4)

    def test_non_positive_doors_is_rejected(self):
        with self.assertRaises(ValueError):
            Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 0)

    def test_empty_make_is_rejected(self):
        with self.assertRaises(ValueError):
            Car("AB12CDE", "  ", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)


class TestVehicleDetails(unittest.TestCase):
    def test_car_details_include_doors(self):
        car = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)
        self.assertIn("Doors: 4", car.get_details())

    def test_van_details_include_capacity(self):
        van = Van("AB12CDE", "Ford", "Transit", "White", 15000, 12000, Branch.SAND, 1200.0)
        self.assertIn("Capacity: 1200.0kg", van.get_details())

    def test_minibus_details_include_seats(self):
        minibus = Minibus("AB12CDE", "Ford", "Transit", "White", 20000, 16000, Branch.TEMPLE, 16)
        self.assertIn("Seats: 16", minibus.get_details())


class TestVehicleSerialisation(unittest.TestCase):
    def test_car_round_trips_through_dict(self):
        car = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)
        rebuilt = vehicle_from_dict(car.to_dict())
        self.assertEqual(car, rebuilt)
        self.assertEqual(rebuilt.doors, 4)
        self.assertIsInstance(rebuilt, Car)

    def test_van_round_trips_through_dict(self):
        van = Van("AB12CDE", "Ford", "Transit", "White", 15000, 12000, Branch.SAND, 1200.0)
        rebuilt = vehicle_from_dict(van.to_dict())
        self.assertEqual(rebuilt.capacity, 1200.0)
        self.assertIsInstance(rebuilt, Van)

    def test_missing_field_raises_invalid_data_error(self):
        data = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4).to_dict()
        del data["doors"]
        with self.assertRaises(InvalidVehicleDataError):
            vehicle_from_dict(data)

    def test_equality_is_based_on_registration_number(self):
        car_a = Car("AB12CDE", "Ford", "Fiesta", "Red", 10000, 8000, Branch.MAIL, 4)
        car_b = Car("AB12CDE", "Toyota", "Corolla", "Blue", 12000, 9000, Branch.SAND, 2)
        self.assertEqual(car_a, car_b)


if __name__ == "__main__":
    unittest.main()
